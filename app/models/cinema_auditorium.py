from app import db

class Auditorium(db.Model):
    __tablename__ = 'auditoriums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)

    seats = db.relationship('Seat', backref='auditorium', lazy=True, cascade="all, delete-orphan")
    cinema_functions = db.relationship('CinemaFunction', back_populates='auditorium', lazy=True)

    def __str__(self):
        return f"""Auditorium (
            id: { self.id },
            name: { self.name },
            total_seats: { self.total_seats },
            <seats>,
            <cinema_functions>
        )"""