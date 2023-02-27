from project import create_app, db
from project.ordering_portal.store import Store
from project.models import User
from datetime import datetime


def test_add_user(add_user_form, store):

    user = store.add_user(form=add_user_form)
    print(user)

    assert user
