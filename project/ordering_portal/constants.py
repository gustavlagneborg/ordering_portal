class FormConstants:
    """Radio fields options for flask forms."""

    MODALITY_OPTIONS = [
        ("MRI", "Magnetic resonance imaging"),
        ("X-ray", "X-ray"),
        ("CT", "Computed tomography"),
    ]

    PSEUDO_OPTIONS = [
        ("Type 1", "Type 1"),
        ("Type 2", "Type 2"),
        ("Type 3", "Type 3"),
        ("No pseudonymisation", "No pseudonymisation"),
    ]

    BODY_PART_OPTIONS = [
        ("Abdomen", "Abdomen"),
        ("Chest", "Chest"),
        ("Scul", "Scul"),
    ]

    DATA_DELIVERY = [("Kaapana", "Kaapana"), ("Raw data", "Raw data")]

    PATIENT_SEX = [
        ("Female", "Female"),
        ("Male", "Male"),
        ("Not relevant", "Not relevant"),
    ]

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
