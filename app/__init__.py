from flask import Flask
from app.models import db
from flask_login import LoginManager
from flask_migrate import Migrate
import logging

login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Setup logging
    logging.basicConfig(level=logging.INFO)  # You can set this to DEBUG for more verbose logging

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.main_routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))