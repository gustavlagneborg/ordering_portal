"""Ordering Portal REST API"""
from flask import jsonify, make_response, request
from . import api_blueprint
from ..OrderingPortal.models import Project, APIUser
from .store import APIStore
from project import db


api_store = APIStore(db=db)


@api_blueprint.route("/")
def index():
    return "Welcome to Ordering Portal REST API"


@api_blueprint.route("/user", methods=["POST"])
def create_api_user():
    data = request.get_json()
    api_user = api_store.add_api_user(data=data)

    return make_response(jsonify({"message": f"New API user {api_user} created!"}), 200)


@api_blueprint.route("/users", methods=["GET"])
def get_all_api_users():
    """Get all api users from the database."""

    api_users = api_store.api_user.query.all()
    output = [api_user.to_dict for api_user in api_users]

    return make_response(jsonify({"users": output}), 200)


@api_blueprint.route("/user/<public_id>", methods=["GET", "DELETE"])
def get_api_user(public_id):
    """Get an api user from the database."""

    api_user: APIUser = api_store.api_user.query.filter_by(public_id=public_id).first()

    if not api_user:
        return make_response(jsonify({"error": "No user found"}), 404)

    if request.method == "GET":
        return make_response(jsonify({"user": api_user.to_dict}), 200)

    if request.method == "DELETE":
        api_store.delete_api_user(api_user=api_user)
        return make_response(jsonify({"message": f"user deleted!"}))


@api_blueprint.route("/projects/<int:id>", methods=["GET"])
def get_project(id):
    """Get endpoint for a single project."""

    project: Project = Project.query.get(id)
    if project:
        return make_response(jsonify(project.to_dict), 200)
    else:
        return make_response(jsonify({"error": "Project not found"}), 404)
