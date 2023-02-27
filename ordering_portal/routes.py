"""Website routes"""

from app import app, db, login_manager
from flask import render_template, flash, redirect, url_for
from forms import ProjectForm, LoginForm, RegistrationForm
from store import Store
from models import User
from flask_login import login_required

store = Store(db=db)


@app.route("/")
@app.route("/home")
def index():
    return render_template("base.html")


@app.route("/order_project", methods=["GET", "POST"])
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


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegistrationForm(csrf_enabled=False)

    if register_form.validate_on_submit():
        user = store.add_user(form=register_form)
        flash(f"{user} successfully added!")
        # return redirect(url_for("register"))

    return render_template("register.html", form=register_form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(csrf_enabled=False)
    user: User = User.query.filter_by(email=login_form.email.data).first()

    if login_form.validate_on_submit():
        if store.login_user(form=login_form):
            return redirect(url_for(".user", username=user.username))
        else:
            flash("Mail or password is incorrect")
            redirect(url_for("login"))

    return render_template("login.html", form=login_form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("logout.html")


@app.route("/user/<username>")
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
