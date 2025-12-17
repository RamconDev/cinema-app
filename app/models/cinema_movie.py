from app import db
from app.models.cinema_movie_genre import MovieGenre

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(250), nullable=True)

    movie_genres = db.relationship('MovieGenre', back_populates="movie", cascade="all, delete-orphan")
    cinema_functions = db.relationship('CinemaFunction', back_populates='movie', lazy=True)