import wtforms_json
import pytest

from project import create_app, db
from project.ordering_portal.forms import RegistrationForm
from project.ordering_portal.store import Store
from sqlalchemy import create_engine




@pytest.fixture(scope="module")
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app(test=True)
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

    yield store # this is where the testing happens!

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

@pytest.fixture(scope='module')
def cli_test_client():
    flask_app = create_app()
    flask_app.config.from_object('config.TestingConfig')

    runner = flask_app.test_cli_runner()

    yield runner  # this is where the testing happens!
