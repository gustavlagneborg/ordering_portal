import pytest
from .mocks import MockAuth


@pytest.fixture()
def add_api_user_data():
    return {"name": "tolvan", "password": "password"}


@pytest.fixture()
def login_auth():
    return MockAuth(username="tolvan", password="password")
