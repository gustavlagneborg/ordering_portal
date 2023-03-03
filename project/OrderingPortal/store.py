"""Store backend in the Ordering Portal"""

import logging
from flask_wtf import FlaskForm
from datetime import datetime
from project.OrderingPortal.models import User
from project.OrderingPortal import models
from flask_login import login_user


LOG = logging.getLogger(__name__)


class Store:
    User = models.User
    Project = models.Project
    Examination = models.Examination

    def __init__(self, db) -> None:
        self.db = db

    def add_user(self, form: FlaskForm) -> User:
        """Add a new user to the database."""
        user = self.User(
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

    def get_examinations(self) -> list[str]:
        """Return all examinations."""
        return [str(examination) for examination in self.Examination.query.all()]
    
