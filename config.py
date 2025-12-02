import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Recomended

    # DB settings
    DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite')
    USER_DB = os.getenv('USER_DB')
    USER_PASSWORD = os.getenv('USER_PASSWORD')
    SERVER_DB = os.getenv('SERVER_DB')
    NAME_DB = os.getenv('NAME_DB')

    # Dinamic url
    if DB_ENGINE.startswith('sqlite'):
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}:///{NAME_DB}.db"  # ej: sqlite:///test.db
    else:
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # Usar una base de datos de prueba en memoria
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'