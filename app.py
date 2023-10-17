from dataclasses import dataclass
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dlpdwqhtwljhbd:67f7bc3a5a19c84cb1aa75860c08db3651b331d70dc99b3116ebd955ccbc064a@ec2-54-211-177-159.compute-1.amazonaws.com:5432/d20858gks9a25j"
db = SQLAlchemy(app)
app.app_context().push()


@dataclass
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100000), nullable=False)
    popularity = db.Column(db.Float, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    entered_at = db.Column(db.DateTime, nullable=False, default=date.today())
    poster_path = db.Column(db.String(100000))

    def __repr__(self):
        return f"Movie: {self.title}"

    def __init__(self, title, popularity, movie_id, poster_path):
        self.title = title
        self.popularity = popularity
        self.movie_id = movie_id
        self.poster_path = poster_path


@dataclass
class TrendingMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100000), nullable=False)
    popularity = db.Column(db.Float, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    entered_at = db.Column(db.DateTime, nullable=False, default=date.today())
    poster_path = db.Column(db.String(100000))

    def __repr__(self):
        return f"Movie: {self.title}"

    def __init__(self, title, popularity, movie_id, poster_path):
        self.title = title
        self.popularity = popularity
        self.movie_id = movie_id
        self.poster_path = poster_path


def getTopMovies():
    response = requests.get(
        "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
    return response.json()["results"]


def getTopTrendingMovies():
    response = requests.get(
        "https://api.themoviedb.org/3/trending/movie/day?language=en-US&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
    return response.json()["results"]


# Adding Top Movies
def addMovies():
    with app.app_context():
        for x in range(0, 10):
            new_entry = Movie(title=getTopMovies()[x]["title"], popularity=getTopMovies()[x]["popularity"],
                              movie_id=getTopMovies()[x]["id"], poster_path=getTopMovies()[x]["poster_path"])
            db.session.add(new_entry)
            db.session.commit()
            print("Movie Added:", getTopMovies()[x]["title"])


# Add Top Trending Movies
def addTrendingMovies():
    with app.app_context():
        for x in range(0, 10):
            new_entry = TrendingMovie(title=getTopTrendingMovies()[x]["title"],
                                      popularity=getTopTrendingMovies()[x]["popularity"],
                                      movie_id=getTopTrendingMovies()[x]["id"],
                                      poster_path=getTopTrendingMovies()[x]["poster_path"])
            db.session.add(new_entry)
            db.session.commit()
            print("Trending Movie Added:", getTopTrendingMovies()[x]["title"])

@app.route('/', methods=['GET'])
def hello():
    return "hello, you have reached a non-functional page"

@app.route('/getTopMoviesNow')
def displayTopMovies():
    return getTopMovies()


@app.route('/getTopTrendingMoviesNow')
def displayTopTrendingMovies():
    return getTopTrendingMovies()

@app.route('/getAllPastTopMovies')
def displayAllPastTopMovies():
    all_movies = Movie.query.all()
    all_movies.reverse()
    movie_details = []
    for movie in all_movies:
        movie_details.append((movie.entered_at, movie.title, movie.movie_id, movie.poster_path, movie.popularity))
    return jsonify(movie_details)

@app.route('/getAllPastTrendingMovies')
def displayAllPastTrendingMovies():
    all_trending_movies = TrendingMovie.query.all()
    all_trending_movies.reverse()
    movie_details = []
    for movie in all_trending_movies:
        movie_details.append((movie.entered_at, movie.title, movie.movie_id, movie.poster_path, movie.popularity))
    return jsonify(movie_details)


with app.app_context():
    trendingMovies = TrendingMovie.query.all()
    movies = Movie.query.all()
    if not movies:
        addMovies()
    if not trendingMovies:
        addTrendingMovies()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(addMovies, "interval", minutes=1)
    scheduler.add_job(addTrendingMovies, "interval", minutes=1)
    #scheduler.add_job(addMovies, "interval", hours=3)
    #scheduler.add_job(addTrendingMovies, "interval", hours=3)
    scheduler.start()


if __name__ == '__main__':
    print("App Starting, printing top movies for today")
    for x in range(0, 10):
        print("Movie", x, ":", getTopMovies()[x]["title"])
    for x in range(0,10):
        print("Trending Movie", x, ":", getTopTrendingMovies()[x]["title"])
    print("Current Time",datetime.utcnow())
    app.run(use_reloader=False, debug=False)
