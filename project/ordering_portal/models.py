"""Declaring database models and relationsships."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from sqlalchemy import types
from .constants import ModelConstants


class User(UserMixin, db.Model):
    """User table."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean)
    external = db.Column(db.Boolean)
    projects = db.relationship("Project", backref="user")

    def __repr__(self):
        """Representaion function."""
        return f"User: {self.username}"

    def set_password(self, password):
        """Function for hashing passowrds."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Function for checking the password against the hasing function."""
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    """Porject table."""

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False, index=True)
    project_status = db.Column(
        types.Enum(ModelConstants.PROJECT_STATUS),
        nullable=False,
        default="Waiting for ethical approval",
    )
    pseudonymisation_type = db.Column(
        types.Enum(ModelConstants.PSEUDONYMISATION_TYPES), nullable=False
    )
    patient_sex = db.Column(types.Enum(ModelConstants.PATIENT_SEX), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Examination(db.Model):
    """Examination table."""

    pass


class ProjectExaminations(db.Model):
    """Association table between Project and Examination."""

    pass


class DataDelivery(db.Model):
    """DataDelivery table."""

    pass


class ProjectDataDelivery(db.Model):
    """Association table between Project and DataDelivery."""

    pass


class Modality(db.Model):
    """Modality Table."""

    pass


class ProjectModalities(db.Model):
    """Association table between Project and Modality."""

    pass


class Remittent(db.Model):
    """Remittent table."""

    pass


class ProjectRemittances(db.Model):
    """Association table between Project and Remittent."""

    pass


class Department(db.Model):
    """Department table."""

    pass


class ProjectDepartments(db.Model):
    """Association table between Project and Department."""

    pass


class Laboratory(db.Model):
    """Laboratory table."""

    pass


class ProjectLaboratories(db.Model):
    """Association table between Project and Department."""

    pass
