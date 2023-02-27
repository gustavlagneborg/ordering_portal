"""Setting up the flask application"""
import os

from click import echo
import sqlalchemy as sa
from flask import Flask
from flask.logging import default_handler
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
db = SQLAlchemy()
login = LoginManager()
login.login_view = "users.login"


# ----------------------------
# Application Factory Function
# ----------------------------
def create_app(config_filename=None):
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database!")
    else:
        app.logger.info("Database already contains the users table.")

    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from ordering_portal.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from ordering_portal.api import api

    app.register_blueprint(api)


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")
