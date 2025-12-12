from app import db

from app.models.auth_role import Role
from app.models.auth_user import User

from app.models.cinema_genre import Genre
from app.models.cinema_movie import Movie

def create_init_data():
    if db.session.execute(db.select(User).filter_by(email='admin@example.com')).scalar_one_or_none() is None:
        roles = [
            Role(name = 'admin', description = "user with all permisions"),
            Role(name = 'client', description = "standard user")
        ]

        users = [
            User.create_user(name = 'administrador', email = 'admin@example.com', password = '123', role_id = 1),
            User.create_user(name = 'user1', email = 'user1@example.com', password = '123'),
            User.create_user(name = 'user2', email = 'user2@example.com', password = '123')
        ]

        genres = [
            Genre(name='action'),
            Genre(name='drama'),
            Genre(name='horror'),
            Genre(name='documentary'),
            Genre(name='comedy'),
            Genre(name='fantasy'),
            Genre(name='animated')
        ]

        movies = [
            Movie(title='Matrix', description="Science fiction action film written and directed by the Wachowskis.", release_year=1999, duration_minutes=110, poster_url=""),
            Movie(title='Lord of The Rings', description="An epic fantasy movie based on the books from J.R.R. Tolkien", release_year=2000, duration_minutes=110, poster_url=""),
            Movie(title='Shrek 2', description="A comedy movie from Dreamworks", release_year=2004, duration_minutes=110, poster_url="")
        ]

        db.session.add_all(roles)
        db.session.add_all(users)
        db.session.add_all(genres)
        db.session.add_all(movies)

        db.session.commit()