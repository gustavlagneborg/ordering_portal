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
    pseudonymisation_type = db.Column(db.Enum(PseudonymisaiontTypes), nullable=False)
    patient_sex = db.Column(db.Enum(PatientSex), nullable=False)
    ordering_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    min_patient_age = db.Column(db.Integer)
    max_patient_age = db.Column(db.Integer)
    radiology_verdict = db.Column(db.Boolean)

    # Association Objects
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    data_deliveries = db.relationship("ProjectDataDeliveries", back_populates="project")
    examinations = db.relationship("ProjectExaminations", back_populates="project")
    modalities = db.relationship("ProjectModalities", back_populates="project")
    remittances = db.relationship("ProjectRemittances", back_populates="project")
    producing_departments = db.relationship(
        "ProjectProducingDepartments", back_populates="project"
    )
    laboratories = db.relationship("ProjectLaboratories", back_populates="project")

    def to_dict(self):
        """Returns a project in json format."""

        return {
            "id:": self.id,
            "Project name:": self.project_name,
            "Project status:": self.project_status,
            "Pseudonymisation type:": self.pseudonymisation_type,
            "Patient sex:": self.patient_sex,
            "Date ordered:": self.ordering_date,
            "Start date:": self.start_date,
            "End date": self.end_date,
            "Minimum patient age:": self.min_patient_age,
            "Maximum patient age:": self.max_patient_age,
            "Radiology verdict:": self.radiology_verdict,
            "User id:": self.user_id,
            "Data Deliveries:": [
                {"Data delivery:": d.data_delivery} for d in self.data_deliveries
            ],
            "Examinations:": [
                {"Examination:": e.examination} for e in self.examinations
            ],
            "Modalities:": [{"Modality:": m.modality} for m in self.modalities],
            "Remittances:": [{"Remittent:": r.remittent} for r in self.remittances]
            if self.remittances
            else None,
            "Producing departments:": [
                {"department:": d.producing_department} for d in self.producing_departments
            ]
            if self.producing_departments
            else None,
            "Laboratories:": [{"Laboratory:": l.laboratory} for l in self.laboratories]
            if self.laboratories
            else None,
        }


class Examination(db.Model):
    """Examination table."""

    id = db.Column(db.Integer, primary_key=True)
    examination = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship("ProjectExaminations", back_populates="examination")

    def __repr__(self) -> str:
        return self.examination


class ProjectExaminations(db.Model):
    """Association table between Project and Examination."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    examination_id = db.Column(
        db.Integer, db.ForeignKey("examination.id"), nullable=False
    )

    # Association Objects
    examination = db.relationship("Examination", back_populates="projects")
    project = db.relationship("Project", back_populates="examinations")


class DataDelivery(db.Model):
    """DataDelivery table."""

    id = db.Column(db.Integer, primary_key=True)
    data_delivery = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship("ProjectDataDeliveries", back_populates="data_delivery")

    def __repr__(self) -> str:
        return self.data_delivery


class ProjectDataDeliveries(db.Model):
    """Association table between Project and DataDelivery."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    data_delivery_id = db.Column(
        db.Integer, db.ForeignKey("data_delivery.id"), nullable=False
    )

    # Association Objects
    data_delivery = db.relationship("DataDelivery", back_populates="projects")
    project = db.relationship("Project", back_populates="data_deliveries")


class Modality(db.Model):
    """Modality Table."""

    id = db.Column(db.Integer, primary_key=True)
    modality = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship("ProjectModalities", back_populates="modality")

    def __repr__(self) -> str:
        return self.modality


class ProjectModalities(db.Model):
    """Association table between Project and Modality."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    modality_id = db.Column(db.Integer, db.ForeignKey("modality.id"), nullable=False)

    # Association Objects
    modality = db.relationship("Modality", back_populates="projects")
    project = db.relationship("Project", back_populates="modalities")


class Remittent(db.Model):
    """Remittent table."""

    id = db.Column(db.Integer, primary_key=True)
    remittent = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship("ProjectRemittances", back_populates="remittent")

    def __repr__(self) -> str:
        return self.remittent


class ProjectRemittances(db.Model):
    """Association table between Project and Remittent."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    remittent_id = db.Column(db.Integer, db.ForeignKey("remittent.id"), nullable=False)

    # Association Objects
    remittent = db.relationship("Remittent", back_populates="projects")
    project = db.relationship("Project", back_populates="remittances")


class ProducingDepartment(db.Model):
    """Producing department table."""

    id = db.Column(db.Integer, primary_key=True)
    producing_department = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship(
        "ProjectProducingDepartments", back_populates="producing_department"
    )

    def __repr__(self) -> str:
        return self.producing_department


class ProjectProducingDepartments(db.Model):
    """Association table between Project and Producing department."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    producing_department_id = db.Column(
        db.Integer, db.ForeignKey("producing_department.id"), nullable=False
    )

    # Association Objects
    producing_department = db.relationship(
        "ProducingDepartment", back_populates="projects"
    )
    project = db.relationship("Project", back_populates="producing_departments")


class Laboratory(db.Model):
    """Laboratory table."""

    id = db.Column(db.Integer, primary_key=True)
    laboratory = db.Column(db.String, index=True, nullable=False)

    # Association Objects
    projects = db.relationship("ProjectLaboratories", back_populates="laboratory")

    def __repr__(self) -> str:
        return self.laboratory


class ProjectLaboratories(db.Model):
    """Association table between Project and Laboratory."""

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    laboratory_id = db.Column(
        db.Integer, db.ForeignKey("laboratory.id"), nullable=False
    )

    # Association Objects
    laboratory = db.relationship("Laboratory", back_populates="projects")
    project = db.relationship("Project", back_populates="laboratories")
