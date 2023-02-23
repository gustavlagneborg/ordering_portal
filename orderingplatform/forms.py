from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    RadioField,
    SelectMultipleField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo
from constants import FormConstants


class ProjectForm(FlaskForm):
    """Form for ordering a project."""

    project_name = StringField(
        "Project name",
        validators=[InputRequired()],
    )
    pseudo_type = RadioField(
        "Pseudonymisation",
        choices=FormConstants.PSEUDO_OPTIONS,
        validators=[InputRequired()],
    )
    modalities = SelectMultipleField(
        "Modality",
        choices=FormConstants.MODALITY_OPTIONS,
        validators=[InputRequired(message="Modalities are required!")],
    )
    examination = SelectMultipleField(
        "Examinations",
        choices=FormConstants.BODY_PART_OPTIONS,
        validators=[InputRequired(message="Examinations are required!")],
    )
    submit = SubmitField("Order projet")


class RegistrationForm(FlaskForm):
    """Form for registring a user"""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    external = BooleanField("External user")
    admin = BooleanField("Admin user")
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Form for loging in a user."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
