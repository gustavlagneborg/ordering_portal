"""Declaring database models and relationsships."""
from app import db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime)
    external = db.Column(db.Boolean)

    def __repr__(self):
        return f"<User: {self.username}>"