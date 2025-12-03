from app import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f'<Movie {self.title} ({self.release_year})>'