import pytest
import os

from click import echo
from datetime import datetime, date
from project.OrderingPortal.forms import RegistrationForm
from project.OrderingPortal.store import Store
from project.api.api_store import APIStore
from project import create_app, db
from project.OrderingPortal.constants import PatientGender, PseudonymisaiontTypes
from project.models import (
    User,
    Examination,
    ProjectExaminations,
    Project,
    DataDelivery,
    ProjectDataDeliveries,
    ProjectModalities,
    Modality,
    Remittent,
    ProjectRemittances,
    ProducingDepartment,
    ProjectProducingDepartments,
    Laboratory,
    ProjectLaboratories,
    APIUser,
)


@pytest.fixture(scope="session")
def test_client():
    """Create a Flask app configured for testing"""

    flask_app = create_app(env="UNIT_TEST")
    flask_app.config.from_object("config.TestingConfig")

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            db.create_all()
            yield testing_client  # this is where the testing happens!

    with flask_app.app_context():
        db.drop_all()

        os.remove(flask_app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""))


@pytest.fixture(scope="session")
def test_store(test_client):
    """Add test data."""

    # add api users
    api_admin_user = APIUser(name="API_Admin", public_id="public-id-admin", admin=True)
    api_admin_user.set_password("apiadmin")

    api_user_gustav = APIUser(name="Gustav", public_id="public-id-gustav")
    api_user_gustav.set_password("test123")
    db.session.add_all([api_admin_user, api_user_gustav])
    db.session.commit()
    echo("API users added!")

    # add users
    admin_user = User(
        firstname="Gustav",
        surname="Lagneborg",
        username="Admin",
        email="admin@admin.se",
        date_joined=datetime.now(),
        admin=True,
    )
    admin_user.set_password("admin")

    # regular user
    gustav = User(
        firstname="Gustav",
        surname="Lagneborg",
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
    kaapana = DataDelivery(data_delivery="Kaapana")
    raw_data = DataDelivery(data_delivery="Raw Data")
    dicom_viewer = DataDelivery(data_delivery="Dicom viewer")

    db.session.add_all([kaapana, raw_data, dicom_viewer])
    db.session.commit()
    echo("Data deliveries added!")

    # add modalities
    ct = Modality(modality="Computed Tomography - CT")
    mri = Modality(modality="Magnetic resonance imaging - MRI")
    x_ray = Modality(modality="X-ray")

    db.session.add_all([ct, mri, x_ray])
    db.session.commit()
    echo("Modalities added!")

    # add remittences
    neuro_huddinge = Remittent(remittent="Neuro Huddinge")
    neuro_solna = Remittent(remittent="Neuro Solna")
    kardiolog_huddinge = Remittent(remittent="Kardiolog Huddinge")
    kardiolog_solna = Remittent(remittent="Kardiolog Solna")

    db.session.add_all(
        [neuro_huddinge, neuro_solna, kardiolog_huddinge, kardiolog_solna]
    )
    db.session.commit()
    echo("Remittences added!")

    # add departments
    neuro_huddinge_d = ProducingDepartment(producing_department="Neuro Huddinge")
    neuro_solna_d = ProducingDepartment(producing_department="Neuro Solna")
    kardiolog_huddinge_d = ProducingDepartment(
        producing_department="Kardiolog Huddinge"
    )
    kardiolog_solna_d = ProducingDepartment(producing_department="Kardiolog Solna")

    db.session.add_all(
        [
            neuro_huddinge_d,
            neuro_solna_d,
            kardiolog_huddinge_d,
            kardiolog_solna_d,
        ]
    )
    db.session.commit()
    echo("Producing departments added!")

    # add laboratories
    lab1 = Laboratory(laboratory="Lab 1")
    lab2 = Laboratory(laboratory="Lab 2")
    lab3 = Laboratory(laboratory="Lab 3")

    db.session.add_all([lab1, lab2, lab3])
    db.session.commit()
    echo("Laboratories added!")

    # add projects
    project1 = Project(
        project_name="Female Sculs",
        pseudonymisation_type="No pseudonymisation",
        patient_gender="Female",
        start_date=date(2000, 1, 1),
        end_date=datetime.now(),
        user_id=gustav.id,
        project_description="This project will examine female sculs",
    )
    db.session.add(project1)
    db.session.commit()

    # add scul examinations to project1
    project1Scul = ProjectExaminations(project=project1, examination=scul)
    db.session.add(project1Scul)

    # add kaapana and dicom viewer as data delivery to project1
    project1Kapana = ProjectDataDeliveries(project=project1, data_delivery=kaapana)
    project1dicom_viewer = ProjectDataDeliveries(
        project=project1, data_delivery=dicom_viewer
    )
    db.session.add_all([project1Kapana, project1dicom_viewer])

    # add modality ct to project 1
    project1_ct = ProjectModalities(project=project1, modality=ct)
    db.session.add(project1_ct)

    # add remittences to proejct 1
    project1_neuro_solna = ProjectRemittances(project=project1, remittent=neuro_solna)
    project1_neuro_huddinge = ProjectRemittances(
        project=project1, remittent=neuro_huddinge
    )
    db.session.add_all([project1_neuro_solna, project1_neuro_huddinge])

    # add departments to project 1
    project1_neuro_solna_d = ProjectProducingDepartments(
        project=project1, producing_department=neuro_solna_d
    )
    project1_neuro_huddinge_d = ProjectProducingDepartments(
        project=project1, producing_department=neuro_huddinge_d
    )
    db.session.add_all([project1_neuro_solna_d, project1_neuro_huddinge_d])

    # add lab 1 to project 1
    project1_lab1 = ProjectLaboratories(project=project1, laboratory=lab1)
    db.session.add(project1_lab1)
    db.session.commit()
    echo("Projects added!")
    echo("Bootstarped the database!")

    echo("__________Project 1__________")
    project1_dict = project1.to_dict
    echo(project1_dict)

    yield db


@pytest.fixture(scope="session")
def store(test_store):
    """Create the database and the database table."""

    return Store(db=db)


@pytest.fixture(scope="session")
def api_store(test_store):
    """Create the database and the database table."""

    return APIStore(db=db)
