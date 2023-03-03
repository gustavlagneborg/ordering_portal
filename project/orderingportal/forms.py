"""Flask forms."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    RadioField,
    SelectMultipleField,
    PasswordField,
    BooleanField,
    DateField,
    IntegerField,
    ValidationError,
    validators,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Email,
    EqualTo,
    NumberRange,
)
from project.orderingportal.constants import FormConstants, ModelConstants


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
        choices=ModelConstants.PSEUDONYMISATION_TYPES,
        validators=[InputRequired()],
    )

    data_delivery = SelectMultipleField(
        "Data delivery",
        choices=FormConstants.DATA_DELIVERY,
        validators=[InputRequired()],
    )


class ExaminationsForm(FlaskForm):
    """Extended form for ordering a project based on examinations."""

    start_date = DateField(
        "Start Date", format="%Y-%m-%d", validators=[InputRequired()]
    )
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[InputRequired()])

    modalities = SelectMultipleField(
        "Modality",
        choices=FormConstants.MODALITY_OPTIONS,
        validators=[InputRequired()],
    )

    examination = SelectMultipleField(
        "Examinations",
        choices=FormConstants.BODY_PART_OPTIONS,
        validators=[InputRequired()],
    )
    patient_sex = SelectMultipleField(
        "Sex", choices=ModelConstants.PATIENT_SEX, validators=[validators.optional()]
    )

    # Optional fields
    patient_age_start = IntegerField(
        "Minimum patient age",
        validators=[NumberRange(min=0, max=150), validators.optional()],
    )
    patient_age_end = IntegerField(
        "Maximum patient age",
        validators=[
            NumberRange(min=0, max=150),
            GreaterThan("patient_age_start"),
            validators.optional(),
        ],
    )
    remittent = SelectMultipleField(
        "Remittent",
        choices=FormConstants.REMITTENT_OPTIONS,
        validators=[validators.optional()],
    )

    producing_department = SelectMultipleField(
        "Producing department",
        choices=FormConstants.PRODUCING_DEPARTMENT,
        validators=[validators.optional()],
    )
    modality_lab = SelectMultipleField(
        "Modality laboratory",
        choices=FormConstants.MODALITY_LABORATORY,
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
