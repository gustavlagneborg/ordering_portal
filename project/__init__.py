"""Setting up the flask application"""
import os

from click import echo
import sqlalchemy as sa
from flask import Flask
from flask.logging import default_handler
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from orderingportal.models import User, Examination, ProjectExaminations, Project
from datetime import datetime


# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
db = SQLAlchemy()
login = LoginManager()
login.login_view = ".login"


# ----------------------------
# Application Factory Function
# ----------------------------
def create_app(env: str):
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    if env == "UNIT_TEST":
        config_type = os.getenv("CONFIG_TYPE", default="config.TestingConfig")
    elif env == "STAGE":
        config_type = os.getenv("CONFIG_TYPE", default="config.StageConfig")
    else:
        config_type = os.getenv("CONFIG_TYPE", default="config.ProductionConfig")

    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)

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
    from project.orderingportal.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.api import api_blueprint
    from project.orderingportal import ordering_portal_blueprint

    app.register_blueprint(ordering_portal_blueprint)
    app.register_blueprint(api_blueprint)


def register_cli_commands(app):
    @app.cli.command("init_db")
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo("Initialized the database!")

    @app.cli.command("bootstrap")
    def bootstrap_data():
        """Bootstrap the database."""
        db.drop_all()
        db.create_all()

        # add users
        admin_user = User(
            username="Admin",
            email="admin@admin.se",
            date_joined=datetime.now(),
            admin=True,
        )
        admin_user.set_password("admin")

        user = User(
            username="Gutav",
            email="gustav@gustav.se",
            date_joined=datetime.now(),
        )
        user.set_password("gustav")

        db.session.add_all([admin_user, user])
        echo("Users added!")

        # add examinations

        # add data delivery

        # add modalities

        # add remittences

        # add departments

        # add laboratores

        # add projects
        echo("Bootstarped the database!")

    @app.cli.command("update_database")
    def bootstrap_data():
        """Update database with master data from Sectra datawarehouse."""

        echo("Database uppdated with master data from Sectra datawarehosue!")
