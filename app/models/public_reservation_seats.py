from app import db

class ReservationSeats(db.Model):
    __tablename__ = "reservation_seats"

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), primary_key=True)
    seat_id =  db.Column(db.Integer, db.ForeignKey('seats.id'), primary_key=True)

    reservation = db.relationship("Reservation", back_populates="reservation_seats")
    seats = db.relationship("Seat", back_populates="reservation_seats")

    def __str__(self):
        return f"""
        ReservationSeats (
            reservation_id: { self.reservation_id },
            seat_id: { self.seat_id }
        )
        """