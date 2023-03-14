import wtforms_json
import pytest

from project import create_app, db
from project.OrderingPortal.forms import RegistrationForm, LoginForm
from project.OrderingPortal.store import Store
from project.OrderingPortal.models import User
from .mocks import MockStore


@pytest.fixture()
def add_user_form():
    wtforms_json.init()

    user: dict = {
        "username": "tolvan2",
        "email": "tolvan2@tolvansson.se",
        "external": False,
        "admin": True,
        "password": "a",
        "password2": "a",
        "submit": False,
    }

    return RegistrationForm.from_json(user)


@pytest.fixture()
def login_form_existing_user():
    wtforms_json.init()

    login: dict = {
        "email": "tolvan2@tolvansson.se",
        "password": "a",
        "remember": True,
        "submit": True,
    }

    return LoginForm.from_json(login)


@pytest.fixture()
def login_form_non_existing_user():
    wtforms_json.init()

    login: dict = {
        "email": "tolvan@trettonsson.se",
        "password": "tolvan",
        "remember": True,
        "submit": True,
    }

    return LoginForm.from_json(login)


@pytest.fixture()
def mock_store():
    return MockStore
