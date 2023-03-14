"""Unit tests for the Ordering Portal Store."""

from project.OrderingPortal.store import Store
from project.OrderingPortal.models import User
from flask_wtf import FlaskForm
from tests.ordering_portal.mocks import MockStore
import logging


def test_add_user(add_user_form: FlaskForm, store: Store, caplog):
    """Test adding a new user."""
    caplog.set_level(logging.INFO)

    # GIVEN a new user
    # WHEN its added to the databse
    user: User = store.add_user(form=add_user_form)

    # THEN a user should be returend and stored in the database
    assert user == store.user.query.filter_by(email=add_user_form.email.data).first()
    assert "successfully added!" in caplog.text


def test_login_existing_user(
    login_form_existing_user: FlaskForm, mock_store: MockStore
):
    """Test loging in a user."""
    # GIVEN a user that exists in a the database
    # WHEN loging in
    login: bool = mock_store.login(form=login_form_existing_user)

    # THEN the user should be logged in
    assert login


def test_login_non_existing_user(
    login_form_non_existing_user: FlaskForm, mock_store: MockStore
):
    """Test loging that doesnt exist."""
    # GIVEN a user that does not exist in a the database
    # WHEN loging in

    login: bool = mock_store.login(form=login_form_non_existing_user)

    # THEN the user should not be logged in
    assert not login
