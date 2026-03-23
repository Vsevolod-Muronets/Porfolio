import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Tuple, Optional

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent


@dataclass
class RecipeMatch:
    title: str
    rating: float
    url: str


@dataclass
class DailyMenuItem:
    course: str
    title: str
    rating: float
    url: str
    ingredients: List[str]
    nutrients: List[Tuple[str, float]]


class NutritionModel:

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or (BASE_DIR / "best_model.pkl")
        self._model = joblib.load(self.model_path)

    def predict_rating(self, ingredients: Iterable[str]) -> str:
        ingredients_list = [ing.strip().lower() for ing in ingredients if ing.strip()]
        ing_set = set(ingredients_list)

        if hasattr(self._model, "feature_names_in_"):
            feature_names = list(self._model.feature_names_in_)
        else:
            sim_csv = BASE_DIR / "similar_recipes.csv"
            with sim_csv.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
            feature_names = [h.strip() for h in header[6:]]

        row: Dict[str, float] = {}
        for name in feature_names:
            key = name.strip()
            row[key] = 1.0 if key.lower() in ing_set else 0.0

        X = pd.DataFrame([row], columns=feature_names)
        prediction = self._model.predict(X)[0]
        return str(prediction)


class RatingInterpreter:

    @staticmethod
    def to_message(label: str) -> str:
        if label == "bad":
            return (
                "You might find it tasty, but in our opinion, it is a bad idea "
                "to have a dish with that list of ingredients."
            )
        if label == "so-so":
            return (
                "It might be okay, but we think this combination of ingredients "
                "will result in a so-so dish."
            )
        return (
            "Both your taste buds and our model agree: this looks like a great "
            "idea for a dish!"
        )


class NutritionTable:

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (BASE_DIR / "daily_data.csv")
        self.daily_values: Dict[str, float] = {}
        self._load()

    def _load(self) -> None:
        with self.csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = str(row["nutrient"]).strip()
                try:
                    value = float(row["value"])
                except (TypeError, ValueError):
                    continue
                if name:
                    self.daily_values[name] = value

    def to_percentages(
        self, nutrient_amounts: Dict[str, float]
    ) -> List[Tuple[str, float]]:
        result: List[Tuple[str, float]] = []
        for name, amount in nutrient_amounts.items():
            daily = self.daily_values.get(name)
            if not daily or daily == 0:
                continue
            percent = 100.0 * amount / daily
            result.append((name, percent))
        result.sort(key=lambda x: x[0].lower())
        return result


class SimilarRecipesFinder:

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (BASE_DIR / "similar_recipes.csv")
        self.titles: List[str] = []
        self.urls: List[str] = []
        self.ratings: np.ndarray
        self.ingredients: List[str] = []
        self.matrix: np.ndarray
        self.breakfast_flags: np.ndarray
        self.lunch_flags: np.ndarray
        self.dinner_flags: np.ndarray
        self._load()

    def _load(self) -> None:
        with self.csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            self.ingredients = [h.strip().lower() for h in header[6:]]
            rows: List[List[float]] = []
            ratings: List[float] = []
            titles: List[str] = []
            urls: List[str] = []
            breakfast_flags: List[float] = []
            lunch_flags: List[float] = []
            dinner_flags: List[float] = []

            for row in reader:
                if not row:
                    continue
                titles.append(row[1])
                urls.append(row[2])
                try:
                    ratings.append(float(row[3]))
                except (TypeError, ValueError):
                    ratings.append(0.0)

                def _flag(value: str) -> float:
                    try:
                        return float(value)
                    except (TypeError, ValueError):
                        return 0.0

                breakfast_flags.append(_flag(row[4]) if len(row) > 4 else 0.0)
                lunch_flags.append(_flag(row[5]) if len(row) > 5 else 0.0)
                dinner_flags.append(_flag(row[6]) if len(row) > 6 else 0.0)

                indicators = [float(x) if x else 0.0 for x in row[6:]]
                rows.append(indicators)

        self.titles = titles
        self.urls = urls
        self.ratings = np.asarray(ratings, dtype=float)
        self.matrix = np.asarray(rows, dtype=float)
        self.breakfast_flags = np.asarray(breakfast_flags, dtype=float)
        self.lunch_flags = np.asarray(lunch_flags, dtype=float)
        self.dinner_flags = np.asarray(dinner_flags, dtype=float)

    def recipe_ingredients(self, index: int) -> List[str]:
        row = self.matrix[index]
        return [name for name, val in zip(self.ingredients, row) if val > 0]

    def top_k(self, ingredients: Iterable[str], k: int = 3) -> List[RecipeMatch]:
        ing_set = {ing.strip().lower() for ing in ingredients if ing.strip()}
        if not ing_set:
            return []

        vec = np.zeros(len(self.ingredients), dtype=float)
        for idx, name in enumerate(self.ingredients):
            if name in ing_set:
                vec[idx] = 1.0

        if not np.any(vec):
            return []

        denom = np.linalg.norm(self.matrix, axis=1) * np.linalg.norm(vec)
        with np.errstate(divide="ignore", invalid="ignore"):
            sims = (self.matrix @ vec) / denom
            sims[~np.isfinite(sims)] = 0.0

        top_idx = np.argsort(-sims)[:k]
        matches: List[RecipeMatch] = []
        for i in top_idx:
            matches.append(
                RecipeMatch(
                    title=self.titles[i],
                    rating=float(self.ratings[i]),
                    url=self.urls[i],
                )
            )
        return matches


def estimate_nutrient_amounts_from_ingredients(
    ingredients: List[str],
) -> Dict[str, float]:
    base_nutrients = ["Protein", "Total carbohydrates", "Fat", "Sodium", "Calcium"]
    amounts: Dict[str, float] = {}
    for _ in ingredients:
        for name in base_nutrients:
            amounts[name] = amounts.get(name, 0.0) + 1.0
    return amounts


class DailyMenuGenerator:

    def __init__(self, finder: SimilarRecipesFinder, nutrition: NutritionTable):
        self.finder = finder
        self.nutrition = nutrition
        self.rng = np.random.default_rng()

    def _recipe_nutrients(self, recipe_index: int) -> List[Tuple[str, float]]:
        ingredients = self.finder.recipe_ingredients(recipe_index)
        amounts = estimate_nutrient_amounts_from_ingredients(ingredients)
        return self.nutrition.to_percentages(amounts)

    def _fits_nutrient_budget(
        self,
        current: Dict[str, float],
        extra: List[Tuple[str, float]],
        max_percent: float = 100.0,
    ) -> bool:
        for name, pct in extra:
            if current.get(name, 0.0) + pct > max_percent:
                return False
        return True

    def _update_nutrient_budget(
        self, current: Dict[str, float], extra: List[Tuple[str, float]]
    ) -> None:
        for name, pct in extra:
            current[name] = current.get(name, 0.0) + pct

    def _pick_for_meal(
        self,
        course: str,
        flags: np.ndarray,
        nutrient_budget: Dict[str, float],
    ) -> DailyMenuItem:
        indices = np.where(flags > 0)[0]
        if indices.size == 0:
            indices = np.arange(len(self.finder.titles))

        sorted_idx = indices[np.argsort(-self.finder.ratings[indices])]
        top = sorted_idx[: min(10, len(sorted_idx))]
        self.rng.shuffle(top)

        chosen = None
        nutrients: List[Tuple[str, float]] = []
        for idx in top:
            candidate_nutrients = self._recipe_nutrients(idx)
            if self._fits_nutrient_budget(nutrient_budget, candidate_nutrients):
                chosen = idx
                nutrients = candidate_nutrients
                break

        if chosen is None:
            chosen = sorted_idx[0]
            nutrients = self._recipe_nutrients(chosen)

        self._update_nutrient_budget(nutrient_budget, nutrients)

        return DailyMenuItem(
            course=course,
            title=self.finder.titles[chosen],
            rating=float(self.finder.ratings[chosen]),
            url=self.finder.urls[chosen],
            ingredients=self.finder.recipe_ingredients(chosen),
            nutrients=nutrients,
        )

    def generate_menu(self) -> List[DailyMenuItem]:
        budget: Dict[str, float] = {}
        items: List[DailyMenuItem] = []

        courses = [
            ("BREAKFAST", self.finder.breakfast_flags),
            ("LUNCH", self.finder.lunch_flags),
            ("DINNER", self.finder.dinner_flags),
        ]

        for course_name, flags in courses:
            items.append(self._pick_for_meal(course_name, flags, budget))

        return items


