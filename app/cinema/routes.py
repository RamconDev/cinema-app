from flask import Blueprint

from app.cinema import cinema_bp as cinema

@cinema.route('/')
def index():
    return "Welcome to the Cinema App!"