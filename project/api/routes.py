"""Ordering Portal REST API"""
from flask import jsonify, make_response, request, Response, send_file
from . import api_blueprint
from ..OrderingPortal.models import Project, APIUser
from .api_store import APIStore
from project import db
from datetime import datetime, timedelta
from functools import wraps
from typing import List

import jwt
import os

api_store = APIStore(db=db)


# ----------------------------
# Custom decorators
# ----------------------------
def token_required(f):
    """Checks if current user have a valid jwt token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = api_store.decode_token(token=api_store.check_jwt_token())
            current_user = APIUser.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Not a valid token!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """Checks if current user have a valid jwt token and is admin."""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            data = api_store.decode_token(token=api_store.check_jwt_token())
            current_user = APIUser.query.filter_by(public_id=data["public_id"]).first()
            assert current_user.admin
        except:
            return jsonify({"message": "Admin only!"}), 403

        return f(current_user, *args, **kwargs)

    return decorated


@api_blueprint.route("/")
def index():
    """Welcome to Ordering Portral API."""

    return "Welcome to Ordering Portal REST API"


# ----------------------------
# GET endpoints
# ----------------------------


@api_blueprint.route("/projects", methods=["GET"])
@token_required
def get_projects(current_user):
    """Get all projects."""

    projects: List[Project] = api_store.project.query.all()
    output = [project.to_dict for project in projects]

    return make_response(jsonify({"projects": output}), 200)


@api_blueprint.route("/projects/<int:id>", methods=["GET"])
@token_required
def get_project(current_user, id):
    """Get a single project."""

    project: Project = api_store.project.query.get(id)
    if project:
        return make_response(jsonify(project.to_dict), 200)
    else:
        return make_response(jsonify({"error": "Project not found"}), 404)


@api_blueprint.route("/users", methods=["GET"])
@token_required
def get_all_api_users(current_user):
    """Get all api users from the database."""

    api_users: List[APIUser] = api_store.api_user.query.all()
    output = [api_user.to_dict for api_user in api_users]

    return make_response(jsonify({"users": output}), 200)


@api_blueprint.route("/projects/<int:id>/pdf", methods=["GET"])
@admin_required
def get_project_pdf(current_user, id):
    """Get the PDF file for a project."""

    project = api_store.project.query.filter_by(id=id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404

    pdf_data = project.generate_project_pdf() # generate the PDF data
    response = Response(pdf_data, content_type='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename={project.project_name}.pdf'

    return response


@api_blueprint.route("/user/<public_id>", methods=["GET"])
@token_required
def get_api_user(current_user, public_id):
    """Get an api user from the database."""

    api_user: APIUser = api_store.api_user.query.filter_by(public_id=public_id).first()

    if not api_user:
        return make_response(jsonify({"error": "No user found"}), 404)
    else:
        return make_response(jsonify({"user": api_user.to_dict}), 200)


# ----------------------------
# POST endpoints
# ----------------------------
@api_blueprint.route("/user", methods=["POST"])
@admin_required
def create_api_user(current_user):
    """Create api user route."""

    data = request.get_json()
    try:
        api_user = api_store.add_api_user(data=data)
    except Exception as e:
        return make_response(jsonify({"Error:": f"{e}"}))

    return make_response(jsonify({"message": f"New API user {api_user} created!"}), 200)


@api_blueprint.route("/login", methods=["POST"])
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
                "exp": datetime.utcnow() + timedelta(days=30),
            },
            os.getenv("SECRET_KEY", default="BAD_SECRET_KEY"),
        )

        return jsonify({"token": token})


# ----------------------------
# PUT endpoints
# ----------------------------
@api_blueprint.route("/projects/<int:id>/status", methods=["PUT"])
@admin_required
def update_project_status(current_user, id):
    """Update the status for a project."""
    print(request.headers.get("Content-Type"))
    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"message": "No status provided"}), 400

    project: Project = api_store.project.query.filter_by(id=id).first()
    if not project:
        return jsonify({"message": "Project not found"}), 404

    try:
        api_store.update_project_status(project=project, new_status=new_status)
        return make_response(
            jsonify(
                {
                    "message": "Project status updated successfully",
                    "project": project.project_name,
                    "status": new_status,
                }
            )
        )
    except Exception as e:
        return make_response(jsonify({"Error:": f"{e}"}))


# ----------------------------
# DELETE endpoints
# ----------------------------
@api_blueprint.route("/user/<public_id>", methods=["DELETE"])
@admin_required
def delete_api_user(current_user, public_id):
    """Get an api user from the database."""

    api_user: APIUser = api_store.api_user.query.filter_by(public_id=public_id).first()

    if not api_user:
        return make_response(jsonify({"error": "No user found"}), 404)
    else:
        try:
            api_store.delete_api_user(api_user=api_user)
            return make_response(jsonify({"message": f"user deleted!"}))
        except Exception as e:
            return make_response(jsonify({"Error:": f"{e}"}))
