"""API and website routes"""

from app import app
from flask import request, render_template

@app.route("/")
def index():
    return render_template("base.html")
    