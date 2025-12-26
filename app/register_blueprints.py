def register_blueprints(app):
    from app.cinema import cinema_bp
    app.register_blueprint(cinema_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.public import public_bp
    app.register_blueprint(public_bp)