from app import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    function_id = db.Column(db.Integer, db.ForeignKey('cinema_function.id'))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='reservation', lazy=True)
    reservation_seats = db.relationship("ReservationSeats", back_populates="reservation", cascade="all, delete-orphan")
    cinema_functions = db.relationship("CinemaFunction", back_populates="reservations")

    def __str__(self):
        return f"""
        Reservation (
            id: { self.id },
            user_id: { self.user_id },
            function_id: { self.function_id },
            create_at: { self.create_at },
            status: { self.status },
            <user>,
            <reservation_seats>,
            <cinema_functions>
        )
        """