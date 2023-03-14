"""Unit tests for API store."""

from project.OrderingPortal.models import APIUser
from project.api.api_store import APIStore
from .mocks import MockAuth

import logging


def test_add_api_user(api_store: APIStore, add_api_user_data: dict, caplog):
    """Test adding a new API user."""

    caplog.set_level(logging.INFO)

    # GIVEN a new API user
    # WHEN its added to the database
    api_user: APIUser = api_store.add_api_user(data=add_api_user_data)

    # THEN a user should be returend and stored in the database
    assert (
        api_user
        == api_store.api_user.query.filter_by(name=add_api_user_data["name"]).first()
    )
    assert "successfully added!" in caplog.text


def test_delete_api_user(api_store: APIStore, caplog):
    """Test for deleting an API user."""

    caplog.set_level(logging.INFO)

    # GIVEN a user to delete
    api_user: APIUser = api_store.api_user.query.all()[0]

    # WHEN deleting the user
    api_store.delete_api_user(api_user=api_user)

    # THE user should not be in the database anymore
    assert api_user not in api_store.api_user.query.all()
    assert "User successfully deleted!" in caplog.text


def test_login(api_store: APIStore, login_auth: MockAuth, caplog):
    """Test for loging in a user"""

    caplog.set_level(logging.INFO)

    api_user: APIUser = api_store.login(auth=login_auth)

    assert api_user
    assert "logged in!" in caplog.text
