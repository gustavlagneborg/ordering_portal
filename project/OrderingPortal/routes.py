"""Website routes"""

from . import ordering_portal_blueprint
from flask import render_template, flash, redirect, url_for
from .forms import ProjectForm, LoginForm, RegistrationForm, ExaminationsForm
from .store import Store
from project.OrderingPortal.models import User
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
    examination_form: ExaminationsForm = ExaminationsForm(csrf_enabled=False)

    if project_form.validate_on_submit and examination_form.validate_on_submit():
        store.add_project(
            examination_form=examination_form,
            project_form=project_form,
            current_user=current_user,
        )

    return render_template(
        "order_project.html",
        project_form=project_form,
        examination_form=examination_form,
    )


@ordering_portal_blueprint.route("/register", methods=["GET", "POST"])
@login_required
def register():
    register_form = RegistrationForm(csrf_enabled=False)

    if current_user.admin:
        if register_form.validate_on_submit():
            user = store.add_user(form=register_form)
            if user:
                flash(f"{user} successfully added!")
            else:
                flash("A user with this email already exists!")

        return render_template("register.html", form=register_form)
    else:
        flash("To access the admin page you need to be an admin!")
        return redirect(url_for(".user"))


@ordering_portal_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Already logged in!  Redirecting to your User Profile page...")
        return redirect(url_for(".user"))

    login_form = LoginForm(csrf_enabled=False)

    if login_form.validate_on_submit():
        if store.login(form=login_form):
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


@ordering_portal_blueprint.route("/admin")
@login_required
def admin():
    if current_user.admin:
        return render_template("admin.html")
    else:
        flash("To access the admin page you need to be an admin!")
        redirect(url_for(".user"))


@ordering_portal_blueprint.route("/about")
def about():
    return render_template("about.html")


@ordering_portal_blueprint.route("/contact")
def contact():
    return render_template("contact.html")
