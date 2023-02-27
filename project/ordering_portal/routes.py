"""Website routes"""

from . import ordering_portal_blueprint
from flask import render_template, flash, redirect, url_for
from .forms import ProjectForm, LoginForm, RegistrationForm
from .store import Store
from project.models import User
from flask_login import current_user, login_required, login_user, logout_user
from project import db

store = Store(db=db)


@ordering_portal_blueprint.route("/")
@ordering_portal_blueprint.route("/home")
def index():
    return render_template("base.html")


@ordering_portal_blueprint.route("/order_project", methods=["GET", "POST"])
@login_required
def order_project():
    """Route for ordering a project."""
    project_form: ProjectForm = ProjectForm(csrf_enabled=False)

    if project_form.validate_on_submit():
        print("Success!")
        print(project_form.startdate.data)
        print(project_form.enddate.data)
        # Log something
        # add_project()
        # return redirect(url_for("user/projects"))

    return render_template("order_project.html", form=project_form)


@ordering_portal_blueprint.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegistrationForm(csrf_enabled=False)

    if register_form.validate_on_submit():
        user = store.add_user(form=register_form)
        flash(f"{user} successfully added!")
        # return redirect(url_for("register"))

    return render_template("register.html", form=register_form)


@ordering_portal_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!  Redirecting to your User Profile page...")
        return redirect(url_for(".user"))

    login_form = LoginForm(csrf_enabled=False)

    if login_form.validate_on_submit():
        if store.login_user(form=login_form):
            return redirect(url_for(".user"))
        else:
            flash("Mail or password is incorrect")
            redirect(url_for(".login"))

    return render_template("login.html", form=login_form)


@ordering_portal_blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))


@ordering_portal_blueprint.route("/user")
@login_required
def user():
    return render_template("user.html", user=current_user)


@ordering_portal_blueprint.route("/about")
def about():
    return render_template("about.html")


@ordering_portal_blueprint.route("/contact")
def contact():
    return render_template("contact.html")