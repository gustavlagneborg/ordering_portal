"""Ordering Portal REST API"""
from flask import jsonify, make_response, request
from . import api_blueprint
from ..OrderingPortal.models import Project


@api_blueprint.route("/")
def index():
    return "Welcome to Ordering Portal REST API"


@api_blueprint.route("/projects/<int:id>", methods=["GET"])
def get_project(id):
    """Get endpoint for a single project."""

    project: Project = Project.query.get(id)
    if project:
        return make_response(jsonify(project.to_dict), 200)
    else:
        return jsonify({"error": "Project not found"}), 404
