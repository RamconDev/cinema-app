from app import db
from datetime import datetime

class CinemaFunction(db.Model):
    __tablename__ = "cinema_function"

    id = db.Column(db.Integer, primary_key=True)
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditoriums.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    start_function = db.Column(db.DateTime, default=datetime.utcnow)
    end_function =  db.Column(db.DateTime, default=datetime.utcnow)

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

    movie = db.relationship("Movie", back_populates="movie_genres")
    genre = db.relationship("Genre", back_populates="movie_genres")