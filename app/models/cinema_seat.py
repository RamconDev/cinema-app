from app import db

class Seat(db.Model):
    __tablename__ = 'seats'

    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(150), nullable=False)
    auditorium_id = db.Column(db.Integer, db.ForeignKey('auditoriums.id'), nullable=False)

    # Restricción de unicidad para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('auditorium_id', 'seat_number', name='_auditorium_seat_uc'),
    )

    def __str__(self):
        return f"seat (seat_number='{ self.seat_number }', auditorium_id='{ self.auditorium_id}')"