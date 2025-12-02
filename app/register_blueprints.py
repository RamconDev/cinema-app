from flask import Blueprint

def register_blueprints(app):
    from app.cinema import cinema_bp
    app.register_blueprint(cinema_bp)