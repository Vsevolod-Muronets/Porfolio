import sys
from pathlib import Path
from typing import List, Dict
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

from recipes import (
    NutritionModel,
    RatingInterpreter,
    NutritionTable,
    SimilarRecipesFinder,
    DailyMenuGenerator,
    estimate_nutrient_amounts_from_ingredients,
)


BASE_DIR = Path(__file__).resolve().parent


def parse_ingredients(argv: List[str]) -> List[str]:
    if not argv:
        return []
    
    joined = " ".join(argv)
    parts = [p.strip() for p in joined.split(",")]
    return [p for p in parts if p]


def run_menu_mode() -> int:

    finder = SimilarRecipesFinder(BASE_DIR / "similar_recipes.csv")
    nutrition_table = NutritionTable(BASE_DIR / "daily_data.csv")
    generator = DailyMenuGenerator(finder, nutrition_table)
    items = generator.generate_menu()

    for item in items:
        print(item.course)
        print("---------------------")
        print(f"{item.title} (rating: {item.rating:.3f})")
        print("Ingredients:")
        for ing in item.ingredients:
            print(f"- {ing}")
        print("Nutrients:")
        for name, pct in item.nutrients:
            print(f"- {name.lower()}: {pct:.0f}%")
        print(f"URL: {item.url}")
    return 0


def main(argv: List[str]) -> int:
    if argv and argv[0] in ("--menu", "-m"):
        return run_menu_mode()

    ingredients = parse_ingredients(argv)
    if not ingredients:
        print("Usage: ./nutritionist.py <ingredient1>, <ingredient2>, ...")
        return 1

    finder = SimilarRecipesFinder(BASE_DIR / "similar_recipes.csv")
    known_ingredients = {name.strip().lower() for name in finder.ingredients}

    valid_ingredients = [
        ing for ing in ingredients if ing.strip().lower() in known_ingredients
    ]
    unknown_ingredients = [
        ing for ing in ingredients if ing.strip().lower() not in known_ingredients
    ]

    if not valid_ingredients:
        print("I. OUR FORECAST")
        print(
            "We could not find any of the specified ingredients in our database. "
            "Please try different ones."
        )
        return 1

    if unknown_ingredients:
        print(
            "the following ingredients are missing in our database: "
            + ", ".join(unknown_ingredients)
        )

    ingredients = valid_ingredients

    model = NutritionModel(BASE_DIR / "best_model.pkl")
    rating_label = model.predict_rating(ingredients)
    message = RatingInterpreter.to_message(rating_label)

    print("I. OUR FORECAST")
    print(message)

    print("II. NUTRITION FACTS")
    nutrition_table = NutritionTable(BASE_DIR / "daily_data.csv")
    nutrient_amounts = estimate_nutrient_amounts_from_ingredients(ingredients)
    nutrient_percents = nutrition_table.to_percentages(nutrient_amounts)

    for ing in ingredients:
        print(ing.capitalize())
        for name, percent in nutrient_percents:
            print(f"{name} - {percent:.0f}% of Daily Value")

    print("III. TOP-3 SIMILAR RECIPES:")
    if rating_label == "bad":
        print(
            "There are no similar recipes to recommend for this combination of ingredients."
        )
        return 0

    matches = finder.top_k(ingredients, k=3)
    if not matches:
        print(
            "There are no similar recipes to recommend for this combination of ingredients."
        )
        return 0

    for m in matches:
        print(f"- {m.title}, rating: {m.rating:.1f}, URL:")
        print(m.url)

    return 0


if __name__ == "__main__":
    import traceback

    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        traceback.print_exc()
        print(f"Error: {exc}")
        raise SystemExit(1)

