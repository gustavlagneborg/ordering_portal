"""Ordering Portal REST API"""
from . import api_blueprint


@api_blueprint.route("/")
def index():
    return "Welcome to Ordering Portal REST API"
