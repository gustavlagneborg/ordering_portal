"""Store backend in the Ordering Portal"""

import logging
from flask_wtf import FlaskForm
from datetime import datetime
from project.OrderingPortal.models import (
    User,
    Project,
    DataDelivery,
    ProjectDataDeliveries,
    ProjectExaminations,
    ProjectModalities,
    Examination,
    Modality,
    Remittent,
    ProjectRemittances,
    ProjectLaboratories,
    Laboratory,
    ProjectProducingDepartments,
    ProducingDepartment,
)
from project.OrderingPortal import models
from project.OrderingPortal.constants import ProjectStatus
from flask_login import login_user
from typing import List


LOG = logging.getLogger(__name__)


class Store:
    """Class for perfomring backend actions between the frontend and database."""

    user = models.User
    project = models.Project
    examination = models.Examination
    data_delivery = models.DataDelivery
    modality = models.Modality
    remittent = models.Remittent
    producing_department = models.ProducingDepartment
    laboratory = models.Laboratory

    def __init__(self, db) -> None:
        self.db = db

    def add_user(self, form: FlaskForm) -> user:
        """Add a new user to the database."""

        if self.user.query.filter_by(email=form.email.data).first():
            return None

        user = self.user(
            username=form.username.data,
            email=form.email.data,
            date_joined=datetime.now(),
            admin=form.admin.data,
            external=form.external.data,
        )
        user.set_password(password=form.password.data)

        self.db.session.add(user)
        self.db.session.commit()
        LOG.info(f"User {user} successfully added!")
        return user

    def login(self, form: FlaskForm) -> bool:
        """Login in a user."""

        user: User = self.user.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            LOG.info(f"User {user} logged in!")
            return True

        return False

    def add_project(
        self,
        project_form: FlaskForm,
        examination_form: FlaskForm,
        current_user: User,
    ):
        """Add project to the database."""

        project: Project = self.project(
            project_name=project_form.project_name.data,
            pseudonymisation_type=project_form.pseudo_type.data[0],
            patient_sex=examination_form.patient_sex.data[0],
            start_date=examination_form.start_date.data,
            end_date=examination_form.end_date.data,
            min_patient_age=examination_form.min_patient_age.data,
            max_patient_age=examination_form.max_patient_age.data,
            radiology_verdict=examination_form.radiology_verdict.data,
            user_id=current_user.id,
        )

        for data_delivery in project_form.data_delivery.data:
            project.set_data_deliveries(
                data_delivery=ProjectDataDeliveries(
                    project=project,
                    data_delivery=self.get_data_delivery(data_delivery=data_delivery),
                )
            )

        for examination in examination_form.examination.data:
            project.set_examinations(
                examination=ProjectExaminations(
                    project=project,
                    examination=self.get_examination(examination=examination),
                )
            )

        for modality in examination_form.modalities.data:
            project.set_modalities(
                modality=ProjectModalities(
                    project=project, modality=self.get_modality(modality=modality)
                )
            )

        for remittent in examination_form.remittent.data:
            project.set_remittances(
                remittent=ProjectRemittances(
                    project=project, remittent=self.get_remittent(remittent=remittent)
                )
            )

        for producing_department in examination_form.producing_department.data:
            project.set_producing_departments(
                producing_department=ProjectProducingDepartments(
                    project=project,
                    producing_department=self.get_producing_department(
                        producing_department=producing_department
                    ),
                )
            )

        for laboratory in examination_form.modality_lab.data:
            project.set_laboratories(
                laboratory=ProjectLaboratories(
                    project=project,
                    laboratory=self.get_laboratory(laboratory=laboratory),
                )
            )

        self.db.session.add(project)
        self.db.session.commit()
        LOG.info(f"Project {project.project_name} successfully added!")

    def get_examinations(self) -> List[str]:
        """Return all examinations."""

        return [str(examination) for examination in self.examination.query.all()]

    def get_examination(self, examination) -> Examination:
        """Return examination."""
        return self.examination.query.filter_by(examination=examination).first()

    def get_data_deliveries(self) -> List[str]:
        """Return all data deliveries."""

        return [str(data_delivery) for data_delivery in self.data_delivery.query.all()]

    def get_data_delivery(self, data_delivery) -> DataDelivery:
        """Return data delivery."""

        return self.data_delivery.query.filter_by(data_delivery=data_delivery).first()

    def get_modalities(self) -> List[str]:
        """Return all modalities."""

        return [str(modality) for modality in self.modality.query.all()]

    def get_modality(self, modality) -> Modality:
        """Return modality."""

        return self.modality.query.filter_by(modality=modality).first()

    def get_remittences(self) -> List[str]:
        """Return all remittences."""

        return [str(remittent) for remittent in self.remittent.query.all()]

    def get_remittent(self, remittent) -> Remittent:
        """Return remittent."""

        return self.remittent.query.filter_by(remittent=remittent).first()

    def get_producing_departments(self) -> List[str]:
        """Return all departments."""

        return [
            str(producing_department)
            for producing_department in self.producing_department.query.all()
        ]

    def get_producing_department(self, producing_department) -> ProducingDepartment:
        """Return producing department."""

        return self.producing_department.query.filter_by(
            producing_department=producing_department
        ).first()

    def get_laboratories(self) -> List[str]:
        """Return all laboratories."""

        return [str(laboratory) for laboratory in self.laboratory.query.all()]

    def get_laboratory(self, laboratory) -> Laboratory:
        """Return Laboratory."""

        return self.laboratory.query.filter_by(laboratory=laboratory).first()
