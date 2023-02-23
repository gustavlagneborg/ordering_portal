"""Website routes"""

from app import app
from flask import request, render_template
from forms import ProjectForm, LoginForm, RegistrationForm
from flask_login import LoginManager, login_required, login_user, logout_user


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
        # Log something
        # add_project()
        # return redirect(url_for("user/projects"))

    return render_template("order_project.html", project_form=project_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register")
def register():
    register_form = RegistrationForm(csrf_enabled=False)

    return render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(csrf_enabled=False)

    if login_form.validate_on_submit():
        print("success!")
    return render_template("login.html", form=login_form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("login.html")


@app.route("/user")
def user():
    return render_template("user.html")
