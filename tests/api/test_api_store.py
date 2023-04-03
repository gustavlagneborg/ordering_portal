"""Unit tests for API store."""

from project.OrderingPortal.models import APIUser, Project, User
from project.api.api_store import APIStore
from .mocks import MockAuth
from project.exec import ProjectStatusError
from typing import List

import pytest
import logging


def test_add_api_user(api_store: APIStore, api_user_data: dict, caplog):
    """Test adding a new API user."""

    caplog.set_level(logging.INFO)

    # GIVEN a new API user
    # WHEN its added to the database
    api_user: APIUser = api_store.add_api_user(data=api_user_data)

    # THEN a user should be returend and stored in the database
    assert (
        api_user
        == api_store.api_user.query.filter_by(name=api_user_data["name"]).first()
    )
    assert "successfully added!" in caplog.text


def test_delete_api_user(api_store: APIStore, caplog):
    """Test for deleting an API user."""

    caplog.set_level(logging.INFO)

    # GIVEN a user to delete
    api_user: APIUser = api_store.api_user.query.all()[0]

    # WHEN deleting the user
    api_store.delete_api_user(api_user=api_user)

    # THEN user should not be in the database anymore
    assert api_user not in api_store.api_user.query.all()
    assert "User successfully deleted!" in caplog.text


def test_login(
    api_store: APIStore, login_auth: MockAuth, add_api_user: APIUser, caplog
):
    """Test for loging in a user"""

    caplog.set_level(logging.INFO)
    # GIVEN an API user
    # WHEN logging in
    api_user: APIUser = api_store.login(auth=login_auth)

    # THEN the user should be logged in
    assert api_user
    assert "logged in!" in caplog.text


def test_update_project_status(api_store: APIStore, valid_project_status, caplog):
    """Test updating project status."""

    caplog.set_level(logging.INFO)
    # GIVEN a project
    project: Project = api_store.project.query.first()

    # WHEN updating the status
    api_store.update_project_status(project=project, new_status=valid_project_status)

    # THEN the status should be updated
    assert valid_project_status == project.project_status.value


def test_update_project_status_fail(
    api_store: APIStore, invalid_project_status, caplog
):
    """Test updating project status."""

    caplog.set_level(logging.INFO)
    # GIVEN a project
    project: Project = api_store.project.query.first()

    # WHEN updating the status with a status that is not valid
    with pytest.raises(ProjectStatusError):
        # THEN the status should not be updated and a ProjectStatusError should be raised
        api_store.update_project_status(
            project=project, new_status=invalid_project_status
        )


def test_get_user_projects(api_store: APIStore):
    """Test getting all projectes for a specific user."""

    # GIVEN a user
    user: User = api_store.user.query.filter_by(id=2).first()

    # WHEN getting projects ordered by that user
    projects: List[Project] = api_store.get_user_projects(user_id=user.id)

    # THEN those projects will be in this list
    assert projects
