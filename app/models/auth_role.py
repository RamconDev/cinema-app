from app import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    users = db.relationship('User', backref='roles', lazy=True)

    @classmethod
    def create_role(cls, name, description=None):
        new_role = cls(
            name=name, 
            description=description
            )
        return new_role