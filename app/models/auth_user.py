from flask_login import UserMixin
from app import db, bcrypt, login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.String(50), db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @classmethod
    def create_user(cls, name, email, password, role_id=2):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = cls(
            name=name, 
            email=email, 
            password_hash=password_hash, 
            role_id=role_id
            )
        return new_user
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))