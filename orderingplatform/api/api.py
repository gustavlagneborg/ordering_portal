"""Orderingplatform REST API"""
from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return "Welcome to Orderingplatform REST API"
