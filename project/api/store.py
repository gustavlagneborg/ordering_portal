from ..OrderingPortal.store import Store
from project.OrderingPortal.models import APIUser
from werkzeug.security import generate_password_hash, check_password_hash

import uuid
import logging

LOG = logging.getLogger(__name__)


class APIStore(Store):
    api_user = APIUser

    def __init__(self, db) -> None:
        super().__init__(db)

    def add_api_user(self, data) -> APIUser:
        """Add a new API user to the database."""

        hashed_password = generate_password_hash(data["password"], method="sha256")
        api_user = APIUser(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            password=hashed_password,
            admin=False,
        )

        self.db.session.add(api_user)
        self.db.session.commit()
        LOG.info(f"User {api_user} successfully added!")
        return api_user

    def delete_api_user(self, api_user: APIUser) -> None:
        """Delete an API user from the database."""

        self.db.session.delete(api_user)
        self.db.session.commit()
        LOG.info(f"User {api_user} successfully deleted!")
