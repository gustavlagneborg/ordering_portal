from project.models import (
    User,
    Project,
    DataDelivery,
    Examination,
    Modality,
    Remittent,
    Laboratory,
    ProducingDepartment,
    APIUser,
)
from project.OrderingPortal.constants import ProjectStatus
from project.exec import ProjectStatusError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, render_template
from typing import List


import os
import jwt
import uuid
import logging

LOG = logging.getLogger(__name__)


class APIStore:
    user = User
    project = Project
    examination = Examination
    data_delivery = DataDelivery
    modality = Modality
    remittent = Remittent
    producing_department = ProducingDepartment
    laboratory = Laboratory
    api_user = APIUser

    def __init__(self, db) -> None:
        self.db = db

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

    def get_user_projects(self, user_id: int) -> List[Project]:
        """Get all projects for a specific user."""

        return self.project.query.filter_by(user_id=user_id).all()

    def update_project_status(self, project: Project, new_status: str):
        """Update a projects status"""

        new_status = new_status.capitalize()

        if new_status not in ProjectStatus.list():
            raise ProjectStatusError(f"Status input {new_status} is not a valid choice")

        if new_status == ProjectStatus.ETHICAL_APPROVAL.value:
            project.project_status = ProjectStatus.ETHICAL_APPROVAL
        elif new_status == ProjectStatus.ETHICAL_APPROVAL_DENIED.value:
            project.project_status = ProjectStatus.ETHICAL_APPROVAL_DENIED
        elif new_status == ProjectStatus.ETHICAL_APPROVAL_APPROVED.value:
            project.project_status = ProjectStatus.ETHICAL_APPROVAL_APPROVED
        elif new_status == ProjectStatus.RETRIEVING_DATA.value:
            project.project_status = ProjectStatus.RETRIEVING_DATA
        elif new_status == ProjectStatus.UPLOADING_DATA.value:
            project.project_status = ProjectStatus.UPLOADING_DATA
        elif new_status == ProjectStatus.UPLOADED.value:
            project.project_status = ProjectStatus.UPLOADED

        self.db.session.commit()
        LOG.info(
            f"Project {project.project_name} status is updated to {project.project_status.value}"
        )
