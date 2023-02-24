"""Ordering Portal REST API"""
from flask import Blueprint

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return "Welcome to Ordering Portal REST API"
