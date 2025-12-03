from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager
from flask_bcrypt import Bcrypt


from config import DevelopmentConfig as Config # to development config
# from config import TestingConfig as Config # to testing config
# from config import Config # to production or default config

from app.register_blueprints import register_blueprints

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app