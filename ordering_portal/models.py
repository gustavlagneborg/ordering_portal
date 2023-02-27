"""Declaring database models and relationsships."""
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """User model for the database"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime)
    admin = db.Column(db.Boolean)
    external = db.Column(db.Boolean)

    def __repr__(self):
        """Representaion function."""
        #return f"User: {self.username}"
        return "Hi"

    def set_password(self, password):
        """Function for hashing passowrds."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Function for checking the password against the hasing function."""
        return check_password_hash(self.password_hash, password)
