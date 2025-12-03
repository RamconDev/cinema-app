from app import db

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    @classmethod
    def create_genre(cls, name, description=None):
        new_genre = cls(
            name=name, 
            description=description
            )
        return new_genre