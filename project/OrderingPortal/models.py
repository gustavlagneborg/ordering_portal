"""Declaring database models and relationsships."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from datetime import datetime
from typing import List
from .constants import ProjectStatus
from project import login


# Flask-Login configuration
@login.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


class APIUser(UserMixin, db.Model):
    """API authenticaed user table."""

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Representaion function."""

        return f"User: {self.name}"

    @property
    def to_dict(self):
        """Return a API user in dict format."""

        return {
            "public_id": self.public_id,
            "name": self.name,
            "admin": self.admin,
        }

    def set_password(self, password):
        """Function for hashing passowrds."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Function for checking the password against the hasing function."""
        return check_password_hash(self.password, password)


class User(UserMixin, db.Model):
    """User table."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    firstname = db.Column(db.String(64), index=True, nullable=False)
    surname = db.Column(db.String(64), index=True, nullable=False)
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
    project_name = db.Column(
        db.String,
        nullable=False,
        index=True,
        unique=True,
    )
    project_status = db.Column(
        db.Enum(ProjectStatus),
        nullable=False,
        default=ProjectStatus.ETHICAL_APPROVAL,
    )
    project_description = db.Column(db.String, nullable=False)
    pseudonymisation_type = db.Column(db.String, nullable=False)
    patient_gender = db.Column(db.String, nullable=False)
    ordering_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now().date()
    )
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    min_patient_age = db.Column(db.Integer)
    max_patient_age = db.Column(db.Integer)
    radiology_verdict = db.Column(db.Boolean, default=False)

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

    def __repr__(self):
        """Representaion function."""
        return self.project_name

    def set_data_deliveries(self, data_delivery):
        self.data_deliveries.append(data_delivery)

    def set_examinations(self, examination):
        self.examinations.append(examination)

    def set_modalities(self, modality):
        self.modalities.append(modality)

    def set_remittances(self, remittent):
        self.remittances.append(remittent)

    def set_producing_departments(self, producing_department):
        self.producing_departments.append(producing_department)

    def set_laboratories(self, laboratory):
        self.laboratories.append(laboratory)

    @property
    def ordering_date_isoformat(self) -> datetime:
        return self.ordering_date.strftime("%Y/%m/%d")

    @property
    def start_date_isoformat(self) -> datetime:
        return self.start_date.strftime("%Y/%m/%d")

    @property
    def end_date_isoformat(self) -> datetime:
        return self.end_date.strftime("%Y/%m/%d")

    @property
    def get_data_deliveries(self) -> List[str]:
        return (
            [{"Data delivery:": str(d.data_delivery)} for d in self.data_deliveries]
            if self.data_deliveries
            else None
        )

    @property
    def get_examinations(self) -> List[str]:
        return (
            [{"Examination:": str(e.examination)} for e in self.examinations]
            if self.examinations
            else None
        )

    @property
    def get_modalities(self) -> List[str]:
        return (
            [{"Modality:": str(m.modality)} for m in self.modalities]
            if self.modalities
            else None
        )

    @property
    def get_remittances(self) -> List[str]:
        return (
            [{"Remittent:": str(r.remittent)} for r in self.remittances]
            if self.remittances
            else None
        )

    @property
    def get_producing_departments(self) -> List[str]:
        return (
            [
                {"department:": str(d.producing_department)}
                for d in self.producing_departments
            ]
            if self.producing_departments
            else None
        )

    @property
    def get_laboratories(self) -> List[str]:
        return (
            [{"Laboratory:": str(l.laboratory)} for l in self.laboratories]
            if self.laboratories
            else None
        )

    @property
    def to_dict(self) -> dict:
        """Returns a project in dict format."""

        return {
            "id": self.id,
            "Project name": self.project_name,
            "Project description": self.project_description,
            "Project status": self.project_status.value,
            "Pseudonymisation type": self.pseudonymisation_type,
            "Patient gender": self.patient_gender,
            "Date ordered": self.ordering_date_isoformat,
            "Start date": self.start_date_isoformat,
            "End date": self.end_date_isoformat,
            "Minimum patient age": self.min_patient_age,
            "Maximum patient age": self.max_patient_age,
            "Radiology verdict": self.radiology_verdict,
            "User": User.query.filter_by(id=self.user_id).first().username,
            "User id": self.user_id,
            "Data Deliveries": self.get_data_deliveries,
            "Examinations": self.get_examinations,
            "Modalities": self.get_modalities,
            "Remittances": self.get_remittances,
            "Producing departments": self.get_producing_departments,
            "Modality laboratories": self.get_laboratories,
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
