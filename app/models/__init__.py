# flask db init
# flask db migrate -m "Creación de modelo User"
# flask db upgrade

# Import auth models
from .auth_user import User
from .auth_role import Role

# Import cinema models
from .cinema_movie import Movie
from .cinema_genre import Genre
from .cinema_movie_genre import MovieGenre
from .cinema_auditorium import Auditorium
from .cinema_seat import Seat