from flask import Blueprint
from project.models import User


ordering_portal_blueprint = Blueprint(
    "ordering_portal",
    __name__,
)


from project import login

# Flask-Login configuration
@login.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

from . import routes
