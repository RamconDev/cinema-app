from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import DevelopmentConfig as Config # to development config
# from config import TestingConfig as Config # to testing config
# from config import Config # to production or default config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # @app.route('/')
    # def index():
    #     return "Hola mundo"

    # Register blueprints
    from app.register_blueprints import register_blueprints
    register_blueprints(app)

    return app