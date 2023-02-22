from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, InputRequired, ValidationError
from constants import FormConstants
from typing import List


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
    examination = SelectMultipleField(
        "Body parts",
        choices=FormConstants.BODY_PART_OPTIONS,
        validators=[InputRequired()],
    )
    submit = SubmitField("Order projet")

    @staticmethod
    def validate_examination(examination: List) -> bool:
        """Validates that examination data is passed in the ProjectForm"""
        if len(examination) == 0:
            return False
        return True
