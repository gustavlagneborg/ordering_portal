from ..OrderingPortal.store import Store
from project.OrderingPortal.models import APIUser
from werkzeug.security import generate_password_hash, check_password_hash

import os
import jwt
import uuid
import logging

LOG = logging.getLogger(__name__)


class APIStore(Store):
    api_user = APIUser

    def __init__(self, db) -> None:
        super().__init__(db)

    def add_api_user(self, data) -> APIUser:
        """Add a new API user to the database."""

        api_user = APIUser(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            admin=False,
        )
        api_user.set_password(data["password"])

        self.db.session.add(api_user)
        self.db.session.commit()
        LOG.info(f"User {api_user} successfully added!")
        return api_user

    def delete_api_user(self, api_user: APIUser) -> None:
        """Delete an API user from the database."""

        self.db.session.delete(api_user)
        self.db.session.commit()
        LOG.info(f"User {api_user} successfully deleted!")

    def login(self, auth) -> APIUser:
        """Login api user."""

        api_user: APIUser = self.api_user.query.filter_by(name=auth.username).first()
        if check_password_hash(api_user.password, auth.password):
            LOG.info(f"API user {api_user} logged in!")
            return api_user
