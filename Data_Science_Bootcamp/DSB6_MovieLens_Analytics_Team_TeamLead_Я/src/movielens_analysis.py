import re
import datetime
from collections import OrderedDict, Counter, defaultdict
import requests
from bs4 import BeautifulSoup
import pytest

class Movies:
    def __init__(self, f_path):
        self.movies=[]
        line_pat = re.compile(r'^(\d+),(?:"([^"]+)"|([^,]+)),(.+)$')
        try:
            with open(f_path,'r',encoding='utf-8') as f:
                try:
                    next(f)
                except StopIteration:
                    print(f"Файл {f_path} пустой")
                    return
                counter=0
                for line in f:
                    counter+=1
                    if counter > 1000:
                        break
                    try:
                        line=line.strip()
                        match=line_pat.match(line)
                        if not match:
                            continue
                        mov_id=int(match.group(1))
                        ttl=match.group(2) if match.group(2) else match.group(3)
                        gnrs=match.group(4).split("|")
                        self.movies.append({'movieID': mov_id, 'title': ttl, 'genres': gnrs})
                    except Exception:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {f_path}")
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу: {f_path}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")

    def dist_by_release(self):
        pat = re.compile(r'\((\d{4})\)')
        yrs_count = {}
        for m in self.movies:
            match = pat.search(m['title'])
            if match:
                yr=match.group(1)
                yrs_count[yr]=yrs_count.get(yr,0)+1
        return OrderedDict(sorted(yrs_count.items(),key=lambda x:x[1],reverse=True))
    
    def dist_by_genres(self):
        gnrs=[]
        for m in self.movies:
            gnrs.extend(m['genres'])
        counts=Counter(gnrs)
        return OrderedDict(sorted(counts.items(),key=lambda x:x[1],reverse=True))
    
    def most_genres(self, n):
        counts={m['title']:len(m['genres']) for m in self.movies}
        srtd_mov=sorted(counts.items(),key=lambda x: x[1], reverse=True)
        return OrderedDict(srtd_mov[:n])

class Ratings:
    def __init__(self,f_path):
        self.ratings=[]
        try:
            with open(f_path,'r',encoding='utf-8') as f:
                try:
                    next(f)
                except StopIteration:
                    print(f"Файл {f_path} пустой")
                    return
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    try:
                        userID,movID,rating,timest=line.strip().split(',')
                        self.ratings.append({'userID':int(userID),'movieID':int(movID),'rating':float(rating),'timestamp':int(timest)})
                    except Exception:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {f_path}")
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу: {f_path}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
    class Movies:
        def __init__(self,ratings):
            self.ratings=ratings
        
        def dist_by_year(self):
            years = [datetime.datetime.fromtimestamp(r['timestamp']).year for r in self.ratings]
            counts=Counter(years)
            return OrderedDict(sorted(counts.items(),key=lambda x: x[0]))
        
        def dist_by_rating(self):
            counts=Counter([r['rating'] for r in self.ratings])
            return OrderedDict(sorted(counts.items(),key=lambda x: x[0]))
        
        def top_by_num_of_ratings(self,n):
            counts=Counter([r['movieID'] for r in self.ratings])
            sorted_counts=counts.most_common(n)
            try:
                movies_obj = Movies('movies.csv')
                id_to_title = {m['movieID']: m['title'] for m in movies_obj.movies}
                sorted_counts = [(id_to_title.get(mid, f'Movie_{mid}'), cnt) for mid, cnt in sorted_counts]
            except:
                pass
            return OrderedDict(sorted_counts)
        
        def top_by_ratings(self,n,metric='average'):
            ratings_per_movie=defaultdict(list)
            for r in self.ratings:
                ratings_per_movie[r['movieID']].append(r['rating'])
            metrics={}
            for mid,vals in ratings_per_movie.items():
                if metric=='median':
                    vals_sorted=sorted(vals)
                    m=len(vals_sorted)
                    if m%2==1:
                        med=vals_sorted[m//2]
                    else:
                        med=(vals_sorted[m//2-1] + vals_sorted[m//2]) / 2
                    metrics[mid]=round(med,2)
                else:
                    metrics[mid]=round(sum(vals)/len(vals),2)
            sorted_metrics=sorted(metrics.items(),key=lambda x: x[1],reverse=True)[:n]
            try:
                movies_obj = Movies('movies.csv')
                id_to_title = {m['movieID']: m['title'] for m in movies_obj.movies}
                sorted_metrics = [(id_to_title.get(mid, f'Movie_{mid}'), val) for mid, val in sorted_metrics]
            except:
                pass
            return OrderedDict(sorted_metrics)
        
        def top_controversial(self,n):
            variances={}
            ratings_per_movie=defaultdict(list)
            for r in self.ratings:
                ratings_per_movie[r['movieID']].append(r['rating'])
            for mid,vals in ratings_per_movie.items():
                mean=sum(vals)/len(vals)
                var=sum((x-mean)**2 for x in vals)/len(vals)
                variances[mid]=round(var,2)
            sorted_var=sorted(variances.items(),key=lambda x: x[1], reverse=True)[:n]
            try:
                movies_obj = Movies('movies.csv')
                id_to_title = {m['movieID']: m['title'] for m in movies_obj.movies}
                sorted_var = [(id_to_title.get(mid, f'Movie_{mid}'), val) for mid, val in sorted_var]
            except:
                pass
            return OrderedDict(sorted_var)
    class Users:
        def __init__(self,ratings):
            self.ratings=ratings
        
        def dist_by_num_of_ratings(self):
            counts=Counter([r['userID'] for r in self.ratings])
            return OrderedDict(sorted(counts.items(),key=lambda x: x[1],reverse=True))
        
        def dist_by_average(self):
            ratings_per_user=defaultdict(list)
            for r in self.ratings:
                ratings_per_user[r['userID']].append(r['rating'])
            avg={u: round(sum(v)/len(v),2) for u,v in ratings_per_user.items()}
            return OrderedDict(sorted(avg.items(),key=lambda x: x[1],reverse=True))
        
        def top_controversial_users(self,n):
            ratings_per_user=defaultdict(list)
            for r in self.ratings:
                ratings_per_user[r['userID']].append(r['rating'])
            variances={}
            for uid,vals in ratings_per_user.items():
                mean=sum(vals)/len(vals)
                var=sum((x-mean)**2 for x in vals)/len(vals)
                variances[uid]=round(var,2)
            sorted_users=sorted(variances.items(),key=lambda x: x[1], reverse=True)[:n]
            return OrderedDict(sorted_users)

class Tags:
    def __init__(self, path_to_the_file):
        self.tags = []
        line_pat = re.compile(r'^(\d+),(\d+),(?:"([^"]*)"|([^,]*)),(\d+)$')
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as f:
                try:
                    next(f)
                except StopIteration:
                    print(f"Файл {path_to_the_file} пустой")
                    return
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    try:
                        line = line.strip()
                        m = line_pat.match(line)
                        if not m:
                            continue
                        tag = m.group(3) if m.group(3) is not None else m.group(4)
                        if tag:
                            self.tags.append(tag.strip())
                    except Exception:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {path_to_the_file}")
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу: {path_to_the_file}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
    
    def most_words(self,n):
        unique=list(set(self.tags))
        counts={t:len(t.split()) for t in unique}
        sorted_tags=sorted(counts.items(),key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_tags)
    
    def longest(self,n):
        unique=list(set(self.tags))
        sorted_tags=sorted(unique,key=len,reverse=True)[:n]
        return sorted_tags
    
    def most_words_and_longest(self,n):
        top_words=set(self.most_words(n).keys())
        top_long=set(self.longest(n))
        return sorted(top_words&top_long)
    
    def most_popular(self,n):
        counts=Counter(self.tags)
        sorted_counts=counts.most_common(n)
        return OrderedDict(sorted_counts)
    
    def tags_with(self,word):
        filtered=sorted({t for t in self.tags if word.lower() in t.lower()})
        return filtered
    
class Links:
    def __init__(self, path_to_the_file):
        self.links = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as f:
                try:
                    next(f)
                except StopIteration:
                    print(f"Файл {path_to_the_file} пустой")
                    return
                for i, line in enumerate(f):
                    if i >= 1000:
                        break
                    try:
                        parts = line.strip().split(',')
                        if len(parts) < 2:
                            continue
                        movie_id = int(parts[0])
                        imdb_id = parts[1]
                        tmdb_id = parts[2] if len(parts) >= 3 and parts[2] != "" else None
                        self.links.append({'movieID': movie_id, 'imdbID': imdb_id, 'tmdbID': tmdb_id})
                    except Exception:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {path_to_the_file}")
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу: {path_to_the_file}")
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")
    
    def get_imdb(self, list_of_movies, list_of_fields):
        imdb_info = []
        movie_to_imdb = {link['movieID']: link['imdbID'] for link in self.links}
        session = requests.Session()
        session.headers.update(self.headers)
        for mid in list_of_movies:
            if mid not in movie_to_imdb:
                continue
            imdb_id = movie_to_imdb[mid]
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            fields = [mid]
            try:
                response = session.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                for field in list_of_fields:
                    field_lower = field.lower()
                    value = "N/A"
                    try:
                        if field_lower == "director":
                            director = soup.find('a', href=lambda x: x and '/name/' in x)
                            if director:
                                value = director.text.strip()
                        elif field_lower == "runtime":
                            runtime_item = soup.find('li', {'data-testid': 'title-techspec_runtime'})
                            if runtime_item:
                                subtext = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                                if subtext:
                                    value = subtext.text.strip()
                                else:
                                    main_span = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                                    if main_span:
                                        value = main_span.text.strip()
                        elif field_lower == "budget":
                            budget_item = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
                            if budget_item:
                                span = budget_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                                if span:
                                    numbers = re.findall(r'[\d,]+', span.text)
                                    if numbers:
                                        value = str(int(numbers[0].replace(',', '')))
                        elif "cumulative worldwide gross" in field_lower:
                            gross_item = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
                            if gross_item:
                                span = gross_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                                if span:
                                    numbers = re.findall(r'[\d,]+', span.text)
                                    if numbers:
                                        value = str(int(numbers[-1].replace(',', '')))
                    except Exception as e:
                        pass
                    fields.append(value)
            except Exception as e:
                fields.extend(["N/A"] * len(list_of_fields))
            imdb_info.append(fields)
        imdb_info.sort(key=lambda x: x[0], reverse=True)
        return imdb_info

    def top_directors(self, n):
        directors = Counter()
        session = requests.Session()
        session.headers.update(self.headers)
        for i, link in enumerate(self.links):
            imdb_id = link['imdbID']
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                director = soup.find('a', href=lambda x: x and '/name/' in x)
                if director:
                    director_name = director.text.strip()
                    directors[director_name] += 1
            except Exception as e:
                continue
        
        sorted_dir = sorted(directors.items(), key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_dir)
    
    def most_expensive(self, n):
        budgets = {}
        session = requests.Session()
        session.headers.update(self.headers)
        for i, link in enumerate(self.links):
            imdb_id = link['imdbID']
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                title_elem = soup.find('h1', {'data-testid': 'hero__pageTitle'})
                title = title_elem.text.strip()
                budget_item = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
                if budget_item:
                    span = budget_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                    if span:
                        numbers = re.findall(r'[\d,]+', span.text)
                        if numbers:
                            budget = int(numbers[0].replace(',', ''))
                            budgets[title] = budget
            except Exception as e:
                continue
        
        sorted_budgets = sorted(budgets.items(), key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_budgets)
    
    def most_profitable(self, n):
        profits = {}
        session = requests.Session()
        session.headers.update(self.headers)
        for i, link in enumerate(self.links):
            imdb_id = link['imdbID']
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                title_elem = soup.find('h1', {'data-testid': 'hero__pageTitle'})
                title = title_elem.text.strip()
                budget_val = None
                gross_val = None
                budget_item = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
                if budget_item:
                    span = budget_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                    if span:
                        numbers = re.findall(r'[\d,]+', span.text)
                        if numbers:
                            budget_val = int(numbers[0].replace(',', ''))
                gross_item = soup.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'})
                if gross_item:
                    span = gross_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                    if span:
                        numbers = re.findall(r'[\d,]+', span.text)
                        if numbers:
                            gross_val = int(numbers[-1].replace(',', ''))
                if budget_val is not None and gross_val is not None:
                    profit = gross_val - budget_val
                    profits[title] = profit
            except Exception as e:
                continue
        
        sorted_profits = sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_profits)
    
    def longest(self, n):
        runtimes = {}
        session = requests.Session()
        session.headers.update(self.headers)
        for i, link in enumerate(self.links):
            imdb_id = link['imdbID']
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                title_elem = soup.find('h1', {'data-testid': 'hero__pageTitle'})
                title = title_elem.text.strip()
                runtime_item = soup.find('li', {'data-testid': 'title-techspec_runtime'})
                if runtime_item:
                    subtext = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                    if subtext:
                        minutes_match = re.search(r'\((\d+)\s*min\)', subtext.text)
                        if minutes_match:
                            total_minutes = int(minutes_match.group(1))
                            if total_minutes > 0:
                                runtimes[title] = total_minutes
                    else:
                        main_span = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                        if main_span:
                            runtime_text = main_span.text.strip()
                            hours = re.search(r'(\d+)\s*h', runtime_text)
                            minutes = re.search(r'(\d+)\s*m', runtime_text)
                            total_minutes = 0
                            if hours:
                                total_minutes += int(hours.group(1)) * 60
                            if minutes:
                                total_minutes += int(minutes.group(1))
                            if total_minutes > 0:
                                runtimes[title] = total_minutes
            except Exception as e:
                continue
        
        sorted_runtimes = sorted(runtimes.items(), key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_runtimes)
    
    def top_cost_per_minute(self, n):
        costs = {}
        session = requests.Session()
        session.headers.update(self.headers)
        for i, link in enumerate(self.links):
            imdb_id = link['imdbID']
            url = f"https://www.imdb.com/title/tt{imdb_id}/"
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.content, 'html.parser')
                title_elem = soup.find('h1', {'data-testid': 'hero__pageTitle'})
                title = title_elem.text.strip() if title_elem else f"Movie_{imdb_id}"
                budget_val = None
                runtime_minutes = None
                budget_item = soup.find('li', {'data-testid': 'title-boxoffice-budget'})
                if budget_item:
                    span = budget_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                    if span:
                        numbers = re.findall(r'[\d,]+', span.text)
                        if numbers:
                            budget_val = int(numbers[0].replace(',', ''))
                runtime_item = soup.find('li', {'data-testid': 'title-techspec_runtime'})
                if runtime_item:
                    subtext = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item--subText')
                    if subtext:
                        minutes_match = re.search(r'\((\d+)\s*min\)', subtext.text)
                        if minutes_match:
                            runtime_minutes = int(minutes_match.group(1))
                    else:
                        main_span = runtime_item.find('span', class_='ipc-metadata-list-item__list-content-item')
                        if main_span:
                            runtime_text = main_span.text.strip()
                            hours = re.search(r'(\d+)\s*h', runtime_text)
                            minutes = re.search(r'(\d+)\s*m', runtime_text)
                            runtime_minutes = 0
                            if hours:
                                runtime_minutes += int(hours.group(1)) * 60
                            if minutes:
                                runtime_minutes += int(minutes.group(1))
                if budget_val is not None and runtime_minutes and runtime_minutes > 0:
                    cost = round(budget_val / runtime_minutes, 2)
                    costs[title] = cost
            except Exception as e:
                continue
        sorted_costs = sorted(costs.items(), key=lambda x: x[1], reverse=True)[:n]
        return OrderedDict(sorted_costs)
    
class Tests:
    @pytest.fixture
    def movies(self):
        return Movies('movies.csv')
    
    def test_dist_by_release_type(self,movies):
        result=movies.dist_by_release()
        assert isinstance(result,dict)
        for k,v in result.items():
            assert isinstance(k,str)
            assert isinstance(v,int)
    
    def test_dist_by_release_sorted(self,movies):
        result=list(movies.dist_by_release().values())
        assert result==sorted(result,reverse=True)

    def test_dist_by_genres_type(self,movies):
        result=movies.dist_by_genres()
        assert isinstance(result,dict)
        for k,v in result.items():
            assert isinstance(k,str)
            assert isinstance(v,int)

    def test_dist_by_genres_sorted(self,movies):
        result=list(movies.dist_by_genres().values())
        assert result==sorted(result, reverse=True)

    def test_most_genres_type(self,movies):
        result=movies.most_genres(5)
        assert isinstance(result,dict)
        for k,v in result.items():
            assert isinstance(k,str)
            assert isinstance(v, int)

    def test_most_genres_sorted(self,movies):
        result=list(movies.most_genres(5).values())
        assert result==sorted(result,reverse=True)

    @pytest.fixture
    def ratings(self):
        return Ratings("ratings.csv")

    @pytest.fixture
    def movies_r(self, ratings):
        return Ratings.Movies(ratings.ratings)

    @pytest.fixture
    def users_r(self, ratings):
        return Ratings.Users(ratings.ratings)

    def test_r_dist_by_year_type(self, movies_r):
        result = movies_r.dist_by_year()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, int)

    def test_r_dist_by_year_sorted(self, movies_r):
        years = list(movies_r.dist_by_year().keys())
        assert years == sorted(years)

    def test_r_dist_by_rating_type(self, movies_r):
        result = movies_r.dist_by_rating()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, float)
            assert isinstance(v, int)

    def test_r_dist_by_rating_sorted(self, movies_r):
        ratings = list(movies_r.dist_by_rating().keys())
        assert ratings == sorted(ratings)

    def test_r_top_by_num_of_ratings_type(self, movies_r):
        result = movies_r.top_by_num_of_ratings(5)
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_r_top_by_num_of_ratings_sorted(self, movies_r):
        counts = list(movies_r.top_by_num_of_ratings(10).values())
        assert counts == sorted(counts, reverse=True)

    def test_r_top_by_ratings_average_type(self, movies_r):
        result = movies_r.top_by_ratings(5, metric="average")
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, float)

    def test_r_top_by_ratings_average_sorted(self, movies_r):
        vals = list(movies_r.top_by_ratings(10, metric="average").values())
        assert vals == sorted(vals, reverse=True)

    def test_r_top_by_ratings_median_type(self, movies_r):
        result = movies_r.top_by_ratings(5, metric="median")
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, float)

    def test_r_top_by_ratings_median_sorted(self, movies_r):
        vals = list(movies_r.top_by_ratings(10, metric="median").values())
        assert vals == sorted(vals, reverse=True)

    def test_r_top_controversial_type(self, movies_r):
        result = movies_r.top_controversial(5)
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, float)

    def test_r_top_controversial_sorted(self, movies_r):
        vals = list(movies_r.top_controversial(10).values())
        assert vals == sorted(vals, reverse=True)

    def test_u_dist_by_num_of_ratings_type(self, users_r):
        result = users_r.dist_by_num_of_ratings()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, int)

    def test_u_dist_by_num_of_ratings_sorted(self, users_r):
        vals = list(users_r.dist_by_num_of_ratings().values())
        assert vals == sorted(vals, reverse=True)

    def test_u_dist_by_average_type(self, users_r):
        result = users_r.dist_by_average()
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, float)

    def test_u_dist_by_average_sorted(self, users_r):
        vals = list(users_r.dist_by_average().values())
        assert vals == sorted(vals, reverse=True)

    def test_u_top_controversial_users_type(self, users_r):
        result = users_r.top_controversial_users(5)
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, int)
            assert isinstance(v, float)

    def test_u_top_controversial_users_sorted(self, users_r):
        vals = list(users_r.top_controversial_users(10).values())
        assert vals == sorted(vals, reverse=True)

    @pytest.fixture
    def tags(self):
        return Tags("tags.csv")

    def test_t_most_words_type(self, tags):
        result = tags.most_words(10)
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_t_most_words_sorted(self, tags):
        vals = list(tags.most_words(10).values())
        assert vals == sorted(vals, reverse=True)

    def test_t_longest_type(self, tags):
        result = tags.longest(10)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_t_longest_sorted(self, tags):
        result = tags.longest(10)
        lengths = [len(x) for x in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_t_most_words_and_longest_type(self, tags):
        result = tags.most_words_and_longest(10)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_t_most_words_and_longest_sorted(self, tags):
        result = tags.most_words_and_longest(10)
        assert result == sorted(result)

    def test_t_most_popular_type(self, tags):
        result = tags.most_popular(10)
        assert isinstance(result, dict)
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_t_most_popular_sorted(self, tags):
        vals = list(tags.most_popular(10).values())
        assert vals == sorted(vals, reverse=True)

    def test_t_tags_with_type(self, tags):
        result = tags.tags_with("fun")
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_t_tags_with_sorted(self, tags):
        result = tags.tags_with("fun")
        assert result == sorted(result)

    def test_t_tags_with_contains_word(self, tags):
        word = "fun"
        result = tags.tags_with(word)
        for t in result:
            assert word.lower() in t.lower()

    @pytest.fixture
    def links(self):
        links_obj = Links("links.csv")
        links_obj.links = links_obj.links[:10]
        return links_obj

    def test_l_get_imdb_type(self, links):
        result = links.get_imdb([1, 2, 3], ["Director", "Budget", "Runtime"])
        assert isinstance(result, list)
        assert len(result) > 0
        for row in result:
            assert isinstance(row, list)
            assert isinstance(row[0], int)
            assert all(isinstance(x, str) for x in row[1:])

    def test_l_get_imdb_sorted_by_movieid_desc(self, links):
        result = links.get_imdb([1, 2, 3, 10], ["Director"])
        assert len(result) > 0
        ids = [row[0] for row in result]
        assert ids == sorted(ids, reverse=True)

    def test_l_top_directors_type(self, links):
        result = links.top_directors(3)
        assert isinstance(result, dict)
        assert len(result) > 0
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_l_top_directors_sorted(self, links):
        result = links.top_directors(3)
        assert len(result) > 0
        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_l_most_expensive_type(self, links):
        result = links.most_expensive(5)
        assert isinstance(result, dict)
        assert len(result) > 0
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_l_most_expensive_sorted(self, links):
        result = links.most_expensive(5)
        assert len(result) > 0
        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_l_most_profitable_type(self, links):
        result = links.most_profitable(5)
        assert isinstance(result, dict)
        assert len(result) > 0
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_l_most_profitable_sorted(self, links):
        result = links.most_profitable(5)
        assert len(result) > 0
        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_l_longest_type(self, links):
        result = links.longest(5)
        assert isinstance(result, dict)
        assert len(result) > 0
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, int)

    def test_l_longest_sorted(self, links):
        result = links.longest(5)
        assert len(result) > 0
        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_l_top_cost_per_minute_type(self, links):
        result = links.top_cost_per_minute(5)
        assert isinstance(result, dict)
        assert len(result) > 0
        for k, v in result.items():
            assert isinstance(k, str)
            assert isinstance(v, float)

    def test_l_top_cost_per_minute_sorted(self, links):
        result = links.top_cost_per_minute(5)
        assert len(result) > 0
        vals = list(result.values())
        assert vals == sorted(vals, reverse=True)

    def test_l_top_cost_per_minute_rounded_2_decimals(self, links):
        result = links.top_cost_per_minute(10)
        assert len(result) > 0
        for v in result.values():
            assert v == round(v, 2)

    
                
if __name__=="__main__":
    pytest.main(["-v", __file__])