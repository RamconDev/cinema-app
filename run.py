from app import create_app
from config import DevelopmentConfig, TestingConfig
from app.init_data import create_init_data

app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    with app.app_context():
        create_init_data()

    app.run()