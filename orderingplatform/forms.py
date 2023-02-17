from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    """Form for ordering a project."""
    order_name: str = StringField("Project name", validators=[DataRequired()])
    pseudonymisation_option = [("Type 1","Type 1"), ("Type 2","Type 2"), ("Type 3","Type 3")]
    pseudonymisation_type = RadioField("Type", choices=pseudonymisation_option)
    submit = SubmitField("Order projet")