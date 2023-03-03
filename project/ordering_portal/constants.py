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


class ModelConstants:
    """Enum constants for SQLalchemy models."""

    PROJECT_STATUS = ()
    PSEUDONYMISATION_TYPES = ("No pseudonymisation", "Type 1", "Type 2")
    PATIENT_SEX = ("Both male and female", "Female", "Male")
