from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, InputRequired
from constants import RadioFieldForms


class ProjectForm(FlaskForm):
    """Form for ordering a project."""

    order_name = StringField("Project name", validators=[DataRequired()])
    modality_type = RadioField(
        "Modality",
        choices=RadioFieldForms.MODALITY_OPTIONS,
        validators=[InputRequired()],
    )
    pseudo_type = RadioField(
        "Pseudonymisation ",
        choices=RadioFieldForms.PSEUDO_OPTIONS,
        validators=[InputRequired()],
    )
    submit = SubmitField("Order projet")
