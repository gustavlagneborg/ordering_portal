"""Store backend in the Ordering Portal"""

import logging
from flask_wtf import FlaskForm
from datetime import datetime
from project.OrderingPortal.models import User
from project.OrderingPortal import models
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
        user = self.user(
            username=form.username.data,
            email=form.email.data,
            date_joined=datetime.now(),
            admin=form.admin.data,
            external=form.external.data,
        )
        user.set_password(form.password.data)

        self.db.session.add(user)
        self.db.session.commit()
        LOG.info(f"User {user} successfully added!")
        return user

    def login(self, form: FlaskForm) -> bool:
        """Login in a user."""

        user: User = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            LOG.info(f"User {user} logged in")
            return True

        return False

    def get_examinations(self) -> List[str]:
        """Return all examinations."""
        return [str(examination) for examination in self.examination.query.all()]

    def get_data_deliveries(self) -> List[str]:
        """Return all data deliveries."""
        return [str(data_delivery) for data_delivery in self.data_delivery.query.all()]

    def get_modalities(self) -> List[str]:
        """Return all modalities."""
        return [str(modality) for modality in self.modality.query.all()]

    def get_remittences(self) -> List[str]:
        """Return all remittences."""
        return [str(remittent) for remittent in self.remittent.query.all()]

    def get_producing_departments(self) -> List[str]:
        """Return all departments."""
        return [str(producing_department) for producing_department in self.producing_department.query.all()]

    def get_laboratories(self) -> List[str]:
        """Return all laboratories."""
        return [str(laboratory) for laboratory in self.laboratory.query.all()]
