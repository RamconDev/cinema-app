from flask import Blueprint

cinema_bp = Blueprint('cinema', __name__, template_folder='templates')

from app.cinema import routes