import wtforms_json
import pytest

from project import create_app, db
from project.ordering_portal.forms import RegistrationForm, LoginForm
from project.ordering_portal.store import Store
from project.models import User
from .mocks import MockStore


@pytest.fixture(scope="module")
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app(env="UNIT_TEST")
    flask_app.config.from_object("config.TestingConfig")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="module")
def store(test_client):
    # Create the database and the database table
    db.create_all()

    store: Store = Store(db=db)

    # add dummy user
    wtforms_json.init()
    user: dict = {
        "username": "tolvan",
        "email": "tolvan@tolvansson.se",
        "external": False,
        "admin": True,
        "password": "tolvan",
        "password2": "tolvan",
        "submit": False,
    }
    user: User = store.add_user(form=RegistrationForm.from_json(user))

    yield store  # this is where the testing happens!

    db.drop_all()


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
        "email": "tolvan@tolvansson.se",
        "password": "tolvan",
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
