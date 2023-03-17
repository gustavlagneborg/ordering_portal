import pytest

from click import echo
from datetime import datetime, date
from project.OrderingPortal.forms import RegistrationForm
from project.OrderingPortal.store import Store
from project.api.api_store import APIStore
from project import create_app, db
from project.OrderingPortal.constants import PatientSex, PseudonymisaiontTypes
from project.OrderingPortal.models import (
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
            # add api users
            api_admin_user = APIUser(
                name="API_Admin", public_id="public-id-admin", admin=True
            )
            api_admin_user.set_password("apiadmin")

            api_user_gustav = APIUser(name="Gustav", public_id="public-id-gustav")
            api_user_gustav.set_password("test123")
            db.session.add_all([api_admin_user, api_user_gustav])
            db.session.commit()
            echo("API users added!")

            # add users
            admin_user = User(
                username="Admin",
                email="admin@admin.se",
                date_joined=datetime.now(),
                admin=True,
            )
            admin_user.set_password("admin")

            # regular user
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
            neuro_huddinge_d = ProducingDepartment(
                producing_department="Neuro Huddinge"
            )
            neuro_solna_d = ProducingDepartment(producing_department="Neuro Solna")
            kardiolog_huddinge_d = ProducingDepartment(
                producing_department="Kardiolog Huddinge"
            )
            kardiolog_solna_d = ProducingDepartment(
                producing_department="Kardiolog Solna"
            )

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

            yield testing_client  # this is where the testing happens!
            db.drop_all()


@pytest.fixture(scope="session")
def store(test_client):
    """Create the database and the database table."""

    return Store(db=db)  # this is where the testing happens!


@pytest.fixture(scope="session")
def api_store(test_client):
    """Create the database and the database table."""

    return APIStore(db=db)  # this is where the testing happens!
