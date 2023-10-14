from typing import Sequence

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://rwashington325:password@localhost/streamingbuddy"
db = SQLAlchemy(app)
app.app_context().push()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100000), nullable=False)
    popularity = db.Column(db.Float, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    entered_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    poster_path = db.Column(db.String(100000))

    def __repr__(self):
        return f"Movie: {self.title}"

    def __init__(self, title, popularity, movie_id, poster_path):
        self.title = title
        self.popularity = popularity
        self.movie_id = movie_id
        self.poster_path =poster_path


def getTopMovies():
    response = requests.get("https://api.themoviedb.org/3/movie/popular?language=en-US&page=1&api_key=de9c1cbc12726b5dfbdf93e65610b6dc")
    #topTenMovies = []
    #for x in range (0,10):
    #    topTenMovies.append(response.json()["results"][x])
    #return topTenMovies
    return response.json()["results"]

def addMovies():
    with app.app_context():
        for x in range (0,10):
            new_entry = Movie(title=getTopMovies()[x]["title"], popularity = getTopMovies()[x]["popularity"], movie_id=getTopMovies()[x]["id"], poster_path=getTopMovies()[x]["poster_path"])
            db.session.add(new_entry)
            db.session.commit()
            print("Movie Added:",getTopMovies()[x]["title"])

@app.route('/getTopMovies')
def displayTopMovies():
    return getTopMovies()

with app.app_context():
    movies = Movie.query.all()
    if not movies:
        addMovies()
    scheduler = BackgroundScheduler()
    scheduler.add_job(addMovies, "interval", days=1)
    scheduler.start()

if __name__ == '__main__':
    print("App Starting, printing top movies for today")
    for x in range (0,10):
       print("Movie",x,":", getTopMovies()[x]["title"])
    app.run(debug=True, use_reloader=False)

