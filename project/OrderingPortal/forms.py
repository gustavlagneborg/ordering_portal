"""Flask forms."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectMultipleField,
    PasswordField,
    BooleanField,
    DateField,
    IntegerField,
    ValidationError,
    validators,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Email,
    EqualTo,
    NumberRange,
)
from project.OrderingPortal.constants import PseudonymisaiontTypes, PatientSex
from project import db
from .store import Store

store = Store(db=db)


class GreaterThan(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """

    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            )
        if field.data is None or other.data is None:
            return None
        if field.data < other.data:  #  --> Change to >= from !=
            d = {
                "other_label": hasattr(other, "label")
                and other.label.text
                or self.fieldname,
                "other_name": self.fieldname,
            }
            message = self.message
            if message is None:
                message = field.gettext(
                    "Maximum patient age must be greater than minimum patient age!"
                )

            raise ValidationError(message % d)


class ProjectForm(FlaskForm):
    """Form for ordering a project."""

    project_name = StringField(
        "Project name",
        validators=[InputRequired()],
    )
    pseudo_type = SelectMultipleField(
        "Pseudonymisation",
        choices=PseudonymisaiontTypes.list(),
        validators=[InputRequired()],
    )
    data_delivery = SelectMultipleField(
        "Data delivery",
        choices=store.get_data_deliveries,
        validators=[InputRequired()],
    )


class ExaminationsForm(FlaskForm):
    """Extended form for ordering a project based on examinations."""

    start_date = DateField(
        "Start Date", format="%Y-%m-%d", validators=[InputRequired()]
    )
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[InputRequired()])

    modalities = SelectMultipleField(
        "Modalities",
        choices=store.get_modalities,
        validators=[DataRequired()],
    )

    examination = SelectMultipleField(
        "Examinations",
        choices=store.get_examinations,
        validators=[InputRequired()],
    )

    patient_sex = SelectMultipleField(
        "Sex", choices=PatientSex.list(), validators=[validators.optional()]
    )

    # Optional fields
    min_patient_age = IntegerField(
        "Minimum patient age",
        validators=[NumberRange(min=0, max=150), validators.optional()],
    )
    max_patient_age = IntegerField(
        "Maximum patient age",
        validators=[
            NumberRange(min=0, max=150),
            GreaterThan("min_patient_age"),
            validators.optional(),
        ],
    )
    remittent = SelectMultipleField(
        "Remittent",
        choices=store.get_remittences,
        validators=[validators.optional()],
    )

    producing_department = SelectMultipleField(
        "Producing department",
        choices=store.get_producing_departments,
        validators=[validators.optional()],
    )
    modality_lab = SelectMultipleField(
        "Modality laboratory",
        choices=store.get_laboratories,
        validators=[validators.optional()],
    )
    radiology_verdict = BooleanField(
        "Verdict from radiologist",
        validators=[validators.optional()],
    )


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
