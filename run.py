from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route("/movie/<title>")
def get_by_title(title):
    return search_by_title(title)


@app.route("/movie/<int:year_start>/to/<int:year_end>")
def search_by_years(year_start: int, year_end: int):
    return jsonify(search_film_by_years(year_start, year_end))


@app.route("/rating/<category>")
def get_films_by_rating(category):
    return jsonify(films_by_rating(category))


@app.route("/genre/<genre>")
def get_movies_by_genre(genre):
    return jsonify(movies_by_genre(genre))


if __name__ == "__main__":
    app.run(debug=True)
