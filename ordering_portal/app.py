"""Setting up the flask application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from api.api import api


app = Flask(__name__)
app.config["SECRET_KEY"] = "!asdasd##"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.register_blueprint(api, url_prefix="/api/v1")

login_manager = LoginManager()
login_manager.init_app(app)

# import models and routes after app is initialized
import routes, models
