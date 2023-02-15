"""API and website routes"""

from app import app
from flask import request, render_template, flash, redirect,url_for

@app.route("/")
def index():
    #return render_template("base.html")
    return "Hello world"