from flask import Blueprint
from flask import render_template

from app.cinema import cinema_bp as cinema

@cinema.route('/')
def index():
    return render_template('index.html')