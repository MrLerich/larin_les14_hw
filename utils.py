import sqlite3
from collections import Counter


PATH = "netflix.db"


class ConnectDB:
    def __init__(self, PATH=PATH):
        self.connect = sqlite3.connect(PATH)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()


def execute_query(query):
    with sqlite3.connect(PATH) as connect:
        cursor = connect.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def search_by_title(title: str):
    """поиск фильма по названию"""
    connect_db = ConnectDB(PATH)
    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title 
            LIKE '%{title}%'
            ORDER BY release_year DESC
            LIMIT 1"""
    connect_db.cursor.execute(query)
    result = connect_db.cursor.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def search_film_by_years(year_start: int, year_end: int) -> list:
    """поиск по диапазону лет выпуска"""
    connect_db = ConnectDB(PATH)
    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year
            BETWEEN {year_start} AND {year_end}
            LIMIT 100             
    """
    connect_db.cursor.execute(query)
    result = connect_db.cursor.fetchall()
    list_of_films = []
    for movie in result:
        list_of_films.append({
            "title": movie[0],
            "release_year": movie[1]
        })
    return list_of_films


def films_by_rating(category: str) -> list:
    """поиск по рейтингу: children, family, adult"""
    connect_db = ConnectDB('netflix.db')
    rating_config = {"children": "'G'",
                     "family": "'G', 'PG', 'PG-13'",
                     "adult": "'R', 'NC-17'"}
    query = f"""
                SELECT title, rating, description 
                FROM netflix 
                WHERE rating IN ({rating_config[category]})"""

    if category not in rating_config:
        return "Переданной группы нет"

    connect_db.cursor.execute(query)
    result = connect_db.cursor.fetchall()
    result_category_lst = []
    for movie in result:
        result_category_lst.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]})
    return result_category_lst


def movies_by_genre(genre: str) -> list:
    """возвращает 10 самых свежих фильмов в формате json"""
    query = f"""
            SELECT title, description 
            FROM netflix 
            WHERE listed_in 
            LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10"""
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({
            "title": f"{movie[0]}",
            "description": f"{movie[1]}"
        })
    return result_list


def cast_partners(actor1: str, actor2: str) -> list:
    """возвращает список актеров, кто играет в паре больше 2 раз"""
    query = f"""
            SELECT `cast` 
            FROM netflix 
            WHERE `cast` 
            LIKE '%{actor1}%' 
            AND `cast` 
            LIKE '%{actor2}%'"""
    result = execute_query(query)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    print(counter)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list


def search_movie_by_param(movie_type: str, release_year: int, genre: str):
    """функция, с помощью которой можно будет передавать тип картины (фильм или сериал),
    год выпуска и ее жанр и получать на выходе список названий картин с их описаниями в JSON"""
    query = f"""
            SELECT title, description 
            FROM netflix 
            WHERE type = '{movie_type}' 
            AND release_year = {release_year} 
            AND listed_in 
            LIKE '%{genre}%'"""
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]})
    return result_list
