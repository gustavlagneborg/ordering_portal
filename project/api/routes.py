"""Ordering Portal REST API"""
from flask import jsonify, make_response, request
from . import api_blueprint
from ..OrderingPortal.models import Project, APIUser
from .store import APIStore
from project import db
from datetime import datetime, timedelta
from functools import wraps

import jwt
import os

api_store = APIStore(db=db)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                token,
                os.getenv("SECRET_KEY", default="BAD_SECRET_KEY"),
                algorithms=["HS256"],
            )
            current_user = APIUser.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@api_blueprint.route("/")
def index():
    """Welcome to Ordering Portral API."""

    return "Welcome to Ordering Portal REST API"


@api_blueprint.route("/login")
def login():
    """Authentication route."""

    auth = request.authorization
    api_user: APIUser = api_store.login(auth=auth)

    if not api_user:
        return make_response(
            "Coult not verify",
            401,
            {"WWW-Authentivate": "Basic realm='Login required!'"},
        )
    else:
        token = jwt.encode(
            {
                "public_id": api_user.public_id,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            os.getenv("SECRET_KEY", default="BAD_SECRET_KEY"),
        )

        return jsonify({"token": token})


@api_blueprint.route("/user", methods=["POST"])
@token_required
def create_api_user(current_user):
    """Create api user route."""

    data = request.get_json()
    api_user = api_store.add_api_user(data=data)

    return make_response(jsonify({"message": f"New API user {api_user} created!"}), 200)


@api_blueprint.route("/users", methods=["GET"])
@token_required
def get_all_api_users(current_user):
    """Get all api users from the database."""

    api_users = api_store.api_user.query.all()
    output = [api_user.to_dict for api_user in api_users]

    return make_response(jsonify({"users": output}), 200)


@api_blueprint.route("/user/<public_id>", methods=["GET", "DELETE"])
@token_required
def get_api_user(current_user, public_id):
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
@token_required
def get_project(current_user, id):
    """Get endpoint for a single project."""

    project: Project = Project.query.get(id)
    if project:
        return make_response(jsonify(project.to_dict), 200)
    else:
        return make_response(jsonify({"error": "Project not found"}), 404)
