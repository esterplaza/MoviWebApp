import os

import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from data_manager import DataManager
from models import db, Movie

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class


@app.route('/')
def index():
    """
    The home page of your application.
    Show a list of all registered users and a form for adding new users.
    """
    users = data_manager.get_users()
    message = request.args.get("message")
    return render_template("index.html", users=users, message=message), 200


@app.route('/users', methods=['POST'])
def create_user():
    """
    Adds a new user to the database.
    The user submits the 'add user' form, and this information is added to
    the database.

    Returns:
        It redirects back to Route ('/').
    """
    name = request.form["name"]
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """
    When the user click on a username, the app retrieves that user’s list of
    favorite movies and displays it.
    """
    movies = data_manager.get_movies(user_id)
    user = data_manager.get_user(user_id)
    if not user:
        return render_template("404.html"), 404
    message = request.args.get("message")
    return render_template("movies.html", movies=movies, user_id=user_id, user_name=user.name, message=message), 200


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a new movie to a user’s list of favorite movies.
    It redirects to the get_movies route.
    """
    user = data_manager.get_user(user_id)
    if not user:
        return render_template("404.html"), 404
    title = request.form["title"]
    year_str = request.form["year"]
    if year_str:
        try:
            add_year = int(year_str)
        except ValueError:
            add_year = None
    else:
        add_year = None
    try:
        url = f"https://www.omdbapi.com/?t={title}&y={add_year}&apikey={API_KEY}"
        response = requests.get(url, timeout=(5, 30))
        add_name = response.json()["Title"]
        add_director = response.json()["Director"]
        add_poster = response.json()["Poster"]
        if not add_year:
            add_year = response.json()["Year"]
    except KeyError:
        return redirect(url_for('get_movies', user_id=user_id, message="❌ The movie was not found"))
    except requests.Timeout:
        return redirect(url_for('get_movies', user_id=user_id, message="❌ Request timed out"))
    except requests.RequestException as e:
        return redirect(url_for('get_movies', user_id=user_id, message=f"❌ Request failed:, {e}"))
    new_movie = Movie(
        name=add_name,
        director=add_director,
        year=add_year,
        poster_url=add_poster,
        user_id=user_id
    )
    data_manager.add_movie(new_movie)
    message = f"✅ The movie {new_movie.name} has been succesfully added."
    return redirect(url_for('get_movies', user_id=user_id, message=message))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Modify the title of a specific movie in a user’s list,
    without depending on OMDb for corrections.
    """
    title = request.form["title"]
    update_status = data_manager.update_movie(movie_id, title)
    if not update_status:
        message=f"❌ The movie with id: {movie_id} was not found"
    else:
        message = f"✅ The movie {title} was successfully updated"
    return redirect(url_for('get_movies', user_id=user_id, message=message))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Remove a specific movie from a user’s favorite movie list.
    """
    delete_status = data_manager.delete_movie(movie_id)
    if not delete_status:
        message=f"❌ The movie with id: {movie_id} was not found"
    else:
        message = f"✅ The movie with ID {movie_id} was deleted."
    return redirect(url_for('get_movies', user_id=user_id, message=message))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
