from app import db

class Auditorium(db.Model):
    __tablename__ = 'auditoriums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)

    seats = db.relationship('Seat', backref='auditorio', lazy=True, cascade="all, delete-orphan")