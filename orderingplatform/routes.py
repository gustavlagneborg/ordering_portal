"""Website routes"""

from app import app
from flask import request, render_template
from forms import ProjectForm


@app.route("/")
@app.route("/home")
def index():
    return render_template("base.html")


@app.route("/order_project", methods=["GET", "POST"])
def order_project():
    """Route for ordering a project."""
    project_form: ProjectForm = ProjectForm(csrf_enabled=False)
    
    print(request.form)

    return render_template("order_project.html", project_form=project_form)


@app.route("/about")
def about():
    return render_template("about.html")
