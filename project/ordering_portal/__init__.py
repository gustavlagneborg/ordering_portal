from flask import Blueprint

ordering_portal_blueprint = Blueprint(
    "ordering_portal", __name__,
)

from . import routes
