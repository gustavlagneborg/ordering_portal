"""Declaring database models and relationsships."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from datetime import datetime
from sqlalchemy import types
from .constants import PatientSex, ProjectStatus, PseudonymisaiontTypes


class User(UserMixin, db.Model):
    """User table."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)
    external = db.Column(db.Boolean, default=False)
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
        db.Enum(ProjectStatus),
        nullable=False,
        default=ProjectStatus.ETHICAL_APPROVAL,
    )
    pseudonymisation_type = db.Column(
        db.Enum(PseudonymisaiontTypes), nullable=False
    )
    patient_sex = db.Column(db.Enum(PatientSex), nullable=False)
    ordering_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    examinations = db.relationship("ProjectExaminations", back_populates="project")
    

class Examination(db.Model):
    """Examination table."""

    id = db.Column(db.Integer, primary_key=True)
    examination = db.Column(db.String, index=True, nullable=False)
    projects = db.relationship("ProjectExaminations", back_populates="examination")

    def __repr__(self):
        return self.examination


class ProjectExaminations(db.Model):
    """Association table between Project and Examination."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    examination_id = db.Column(
        db.Integer, db.ForeignKey("examination.id"), nullable=False
    )
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    examination = db.relationship("Examination", back_populates="projects")
    project = db.relationship("Project", back_populates="examinations")


# class DataDelivery(db.Model):
#     """DataDelivery table."""

#     pass


# class ProjectDataDelivery(db.Model):
#     """Association table between Project and DataDelivery."""

#     pass


# class Modality(db.Model):
#     """Modality Table."""

#     pass


# class ProjectModalities(db.Model):
#     """Association table between Project and Modality."""

#     pass


# class Remittent(db.Model):
#     """Remittent table."""

#     pass


# class ProjectRemittances(db.Model):
#     """Association table between Project and Remittent."""

#     pass


# class Department(db.Model):
#     """Department table."""

#     pass


# class ProjectDepartments(db.Model):
#     """Association table between Project and Department."""

#     pass


# class Laboratory(db.Model):
#     """Laboratory table."""

#     pass


# class ProjectLaboratories(db.Model):
#     """Association table between Project and Department."""

#     pass""
