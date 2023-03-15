import wtforms_json
import pytest
import datetime

from project.OrderingPortal.forms import RegistrationForm, LoginForm, ExaminationsForm, ProjectForm
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
def project_form():
    wtforms_json.init()
    project_form: ProjectForm = {
        "project_name": "Test project",
        "pseudo_type": ["No pseudonymisation"],
        "data_delivery": ["Kaapana"],
        "csrf_token": "ImMyMzVmMmIwN2UwN2RlNDNjYTI2MmJlYmE0MDZkZGEzZmFkMjRmMTIi.ZBGvvg.LoZYRve7r1cQnDXgopil2vSKw94",
    }
    return ProjectForm.from_json(project_form)


@pytest.fixture()
def examination_form():

    wtforms_json.init()
    examination_form: dict = {
        "start_date": "2011-03-25",
        "end_date": "2023-3-15",
        "modalities": ["Computed Tomography - CT"],
        "examination": ["Scul"],
        "patient_sex": ["Male"],
        "min_patient_age": 1,
        "max_patient_age": 2,
        "remittent": ["Neuro Huddinge", "Neuro Solna"],
        "producing_department": ["Neuro Huddinge", "Neuro Solna"],
        "modality_lab": ["Lab 1"],
        "radiology_verdict": False,
        "csrf_token": "ImMyMzVmMmIwN2UwN2RlNDNjYTI2MmJlYmE0MDZkZGEzZmFkMjRmMTIi.ZBGvvg.LoZYRve7r1cQnDXgopil2vSKw94",
    }
    return ExaminationsForm.from_json(examination_form)


@pytest.fixture()
def project_user(store, project_user_form):
    return store.add_user(form=project_user_form)


@pytest.fixture()
def project_user_form():
    wtforms_json.init()

    user: dict = {
        "username": "tolva3",
        "email": "tolvan3@tolvansson.se",
        "external": False,
        "admin": True,
        "password": "a",
        "password2": "a",
        "submit": False,
    }

    return RegistrationForm.from_json(user)


@pytest.fixture()
def mock_store():
    return MockStore
