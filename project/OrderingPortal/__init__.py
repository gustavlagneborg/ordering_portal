from flask import Blueprint
from project import db
from click import echo
from datetime import datetime
from .models import User, Examination, ProjectExaminations, Project
from .constants import PatientSex, ProjectStatus, PseudonymisaiontTypes


ordering_portal_blueprint = Blueprint(
    "ordering_portal",
    __name__,
)

from . import routes


@ordering_portal_blueprint.cli.command("bootstrap")
def bootstrap_data():
    """Bootstrap the database."""
    db.drop_all()
    db.create_all()

    # add users
    admin_user = User(
        username="Admin",
        email="admin@admin.se",
        date_joined=datetime.now(),
        admin=True,
    )
    admin_user.set_password("admin")
    db.session.add(admin_user)

    gustav = User(
        username="Gustav",
        email="gustav@gustav.se",
        date_joined=datetime.now(),
    )
    gustav.set_password("gustav")

    db.session.add_all([admin_user, gustav])
    db.session.commit()
    echo("Users added!")

    # add examinations
    abdomen = Examination(examination="Abdomen")
    chest = Examination(examination="Chest")
    scul = Examination(examination="Scul")

    db.session.add_all([scul, chest, abdomen])
    db.session.commit()
    echo("Examinations added!")

    # add data delivery

    # add modalities

    # add remittences

    # add departments

    # add laboratores

    # add projects
    project1 = Project(
        project_name="Female Sculs",
        pseudonymisation_type=PseudonymisaiontTypes.NO_PESUDO,
        patient_sex=PatientSex.FEMALE,
        user_id=gustav.id,
    )

    db.session.add(project1)
    db.session.commit()

    # add scul examinations to project1
    project1Scul = ProjectExaminations(project=project1, examination=scul)
    db.session.add(project1Scul)
    db.session.commit()
    
    echo("Projects added!")
    echo("Bootstarped the database!")


@ordering_portal_blueprint.cli.command("update_database")
def update_database():
    """Update database with master data from Sectra datawarehouse."""

    echo("Database uppdated with master data from Sectra datawarehosue!")
