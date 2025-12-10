from app import db

class MovieGenre(db.Model):
    __tablename__ = "movie_genre"

    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

    movie = db.relationship("Movie", back_populates="movie_genres")
    genre = db.relationship("Genre", back_populates="movie_genres")

    @classmethod
    def create_genre(cls, movie_id, genre_id):
        new_movie_genre = cls(
            movie_id=movie_id, 
            genre_id=genre_id
            )
        return new_movie_genre