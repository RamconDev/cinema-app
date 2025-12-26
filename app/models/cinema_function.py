from app import db
from datetime import datetime

class CinemaFunction(db.Model):
    __tablename__ = "cinema_function"

    id = db.Column(db.Integer, primary_key=True)
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditoriums.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    start_function = db.Column(db.DateTime, default=datetime.utcnow)
    end_function =  db.Column(db.DateTime, default=datetime.utcnow)

    movie = db.relationship("Movie", back_populates="cinema_functions")
    auditorium = db.relationship("Auditorium", back_populates="cinema_functions")
    reservations = db.relationship("Reservation", back_populates="cinema_functions")

    def __str__(self):
        return f"""
        CinemaFunction (
            id: { self.id },
            auditorium_id: { self.auditorium_id },
            movie_id: { self.movie_id },
            start_function: { self.start_function },
            end_function: { self.end_function },
            <movie>,
            <auditorium>,
            <reservations>
        )
        """