from enum import Enum


class FormConstants:
    """Choices for flask forms."""

    MODALITY_OPTIONS = [
        ("MRI", "Magnetic resonance imaging"),
        ("X-ray", "X-ray"),
        ("CT", "Computed tomography"),
    ]

    BODY_PART_OPTIONS = [
        ("Abdomen", "Abdomen"),
        ("Chest", "Chest"),
        ("Scul", "Scul"),
    ]

    DATA_DELIVERY = [("Kaapana", "Kaapana"), ("Raw data", "Raw data")]

    REMITTENT_OPTIONS = [
        ("Neuro Huddinge", "Neuro Huddinge"),
        ("Neuro Solna", "Neuro Solna"),
        ("Kardiolog Solna", "Kardiolog Solna"),
        ("Kardiolog Huddinge", "Kardiolog Huddinge"),
    ]

    PRODUCING_DEPARTMENT = [
        ("Neuro Huddinge", "Neuro Huddinge"),
        ("Neuro Solna", "Neuro Solna"),
        ("Kardiolog Solna", "Kardiolog Solna"),
        ("Kardiolog Huddinge", "Kardiolog Huddinge"),
    ]

    MODALITY_LABORATORY = [
        ("Lab 1", "Lab 1"),
        ("Lab 2", "Lab 2"),
        ("Lab 3", "Lab 3"),
    ]

    PSEUDONYMISATION_TYPES = [
        ("No pseudonymisation", "No pseudonymisation"),
        ("Type 2", "Type 2"),
        ("Type 3", "Type 3"),
    ]

    PATIENT_SEX = [
        ("Both", "Both"),
        ("Male", "Male"),
        ("Female", "Female"),
    ]


class ProjectStatus(Enum):
    ETHICAL_APPROVAL="Waiting for ethical approval"
    RETRIEVING_DATA = "Retrieving data"
    UPLOADED = "Uploaded to data delivery"

class PseudonymisaiontTypes(Enum):
    NO_PESUDO = "No pseudonymisation"
    TYPE1 = "Type 1"
    TYPE2 = "Type 2"

class PatientSex(Enum):
    MALE = "Male"
    FEMALE = "Female"
    BOTH = "Both"

