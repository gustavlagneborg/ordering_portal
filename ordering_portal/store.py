"""Store backend in the Ordering Portal"""

from datetime import datetime
import logging
from models import User
from forms import RegistrationForm


LOG = logging.getLogger(__name__)


class Store:
    def __init__(self, db) -> None:
        self.db = db

    def add_user(self, form: RegistrationForm):
        """Add a new user to the database."""
        user = User(
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
