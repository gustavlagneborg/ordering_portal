from ..OrderingPortal.store import Store
from project.OrderingPortal.models import APIUser
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify

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
        LOG.info(f"User successfully deleted!")

    def login(self, auth) -> APIUser:
        """Login api user."""

        api_user: APIUser = self.api_user.query.filter_by(name=auth.username).first()
        if api_user.check_password(auth.password):
            LOG.info(f"API user {api_user} logged in!")
            return api_user

    def check_jwt_token(self):
        """Check if jwt token exists in request."""

        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        else:
            return token

    def decode_token(self, token):
        """Decode jwt doken."""
        
        return jwt.decode(
            token,
            os.getenv("SECRET_KEY", default="BAD_SECRET_KEY"),
            algorithms=["HS256"],
        )
