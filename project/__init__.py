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
def create_app(test: bool = False):
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    if test == True:
        config_type = os.getenv("CONFIG_TYPE", default="config.TestingConfig")
    else:
        config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")

    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
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
    from project.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.api import api_blueprint
    from project.ordering_portal import ordering_portal_blueprint

    app.register_blueprint(ordering_portal_blueprint)
    app.register_blueprint(api_blueprint)


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")

