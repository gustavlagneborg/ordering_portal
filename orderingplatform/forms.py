from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, InputRequired
from constants import FormConstants

class ProjectForm(FlaskForm):
    """Form for ordering a project."""

    order_name = StringField("Project name", validators=[DataRequired()])
    modality_type = RadioField(
        "Modality",
        choices=FormConstants.MODALITY_OPTIONS,
        validators=[InputRequired()],
    )
    pseudo_type = RadioField(
        "Pseudonymisation ",
        choices=FormConstants.PSEUDO_OPTIONS,
        validators=[InputRequired()],
    )

    multiselect = SelectMultipleField("Body parts",
        choices=FormConstants.BODY_PART_OPTIONS
    )
    submit = SubmitField("Order projet")
