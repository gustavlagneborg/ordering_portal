import pytest
from .mocks import MockAuth
from project.api.api_store import APIStore
from project.OrderingPortal.models import APIUser


@pytest.fixture()
def api_user_data():
    return {"name": "tolvan", "password": "password"}


@pytest.fixture()
def login_user_data():
    return {"name": "tolvan2", "password": "password"}


@pytest.fixture()
def login_auth():
    return MockAuth(username="tolvan2", password="password")


@pytest.fixture()
def add_api_user(api_store: APIStore, login_user_data: dict) -> APIUser:
    return api_store.add_api_user(data=login_user_data)


@pytest.fixture()
def valid_project_status() -> str:
    return "Uploaded"


@pytest.fixture()
def invalid_project_status() -> str:
    return "uppploaded"
