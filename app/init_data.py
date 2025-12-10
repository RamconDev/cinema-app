from app import db

from app.models.auth_role import Role
from app.models.auth_user import User

from app.models.cinema_genre import Genre
from app.models.cinema_movie import Movie

def create_init_data():
    if db.session.execute(db.select(User).filter_by(email='admin@example.com')).scalar_one_or_none() is None:
        roles = [
            Role(
                name = 'admin', 
                description = "user with all permisions"
            ),
            Role(
                name = 'client', 
                description = "standard user"
            )
        ]

        users = [
            User.create_user(
                name = 'administrador', 
                email = 'admin@example.com', 
                password = '123',
                role_id = 1
            ),
            User.create_user(
                name = 'user1', 
                email = 'user1@example.com', 
                password = '123'
            ),
            User.create_user(
                name = 'user2', 
                email = 'user2@example.com', 
                password = '123'
            )
        ]

        genres = [
            Genre(name='action'),
            Genre(name='drama'),
            Genre(name='horror'),
            Genre(name='documentary'),
            Genre(name='comedy'),
            Genre(name='fantasy')
        ]

        db.session.add_all(roles)
        db.session.add_all(users)
        db.session.add_all(genres)

        db.session.commit()