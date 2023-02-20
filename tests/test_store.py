#!/usr/bin/env python

from flask import Flask, render_template_string, request
from wtforms import Form, SelectMultipleField

application = app = Flask("wsgi")


class LanguageForm(Form):
    language = SelectMultipleField(
        "Programming Language",
        choices=[("cpp", "C++"), ("py", "Python"), ("text", "Plain Text")],
    )


template_form = """
{% block content %}
<h1>Set Language</h1>

<form method="POST" action="/">
    <div>{{ form.language.label }} {{ form.language(rows=3, multiple=True) }}</div>
    <button type="submit" class="btn">Submit</button>    
</form>
{% endblock %}

"""

completed_template = """
{% block content %}
<h1>Language Selected</h1>

<div>{{ language }}</div>

{% endblock %}

"""


@app.route("/", methods=["GET", "POST"])
def index():
    form = LanguageForm(request.form)
