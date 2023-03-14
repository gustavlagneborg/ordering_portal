
import pytest
import wtforms_json

from project.OrderingPortal.forms import RegistrationForm
from project.OrderingPortal.store import Store
from project.OrderingPortal.models import User
from project import create_app, db


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