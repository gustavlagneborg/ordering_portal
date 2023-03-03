"""Store backend in the Ordering Portal"""

import logging

from datetime import datetime
from project.ordering_portal.models import User
from project.ordering_portal import models
from project.ordering_portal.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user


LOG = logging.getLogger(__name__)


class Store:
    User = models.User
    # Project = modesl.Project etc ...

    def __init__(self, db) -> None:
        self.db = db

    def add_user(self, form: RegistrationForm) -> User:
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

    def login(self, form: LoginForm) -> bool:
        """Login in a user."""

        user: User = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            LOG.info(f"User {user} logged in")
            return True

        return False
