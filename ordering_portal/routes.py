"""Website routes"""

from app import app, db
from flask import render_template, flash, redirect, url_for
from forms import ProjectForm, LoginForm, RegistrationForm
from store import Store
from flask_login import LoginManager, login_required, login_user, logout_user

store = Store(db=db)


@app.route("/")
@app.route("/home")
def index():
    return render_template("base.html")


@app.route("/order_project", methods=["GET", "POST"])
# @login_required
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


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegistrationForm(csrf_enabled=False)

    if register_form.validate_on_submit():
        store.add_user(form=register_form)
        flash("User successfully added!")
        return redirect(url_for("register"))

    return render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(csrf_enabled=False)

    if login_form.validate_on_submit():
        print("success!")

    return render_template("login.html", form=login_form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("logout.html")


@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
