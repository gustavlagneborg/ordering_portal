class FormConstants:
    """Radio fields options for flask forms."""

    MODALITY_OPTIONS = [
        ("MRI", "Magnetic resonance imaging"),
        ("X-ray", "X-ray"),
        ("CT", "Computed tomography"),
    ]

    PSEUDO_OPTIONS = [
        ("No pseudonymisation", "No pseudonymisation"),
        ("Type 1", "Type 1"),
        ("Type 2", "Type 2"),
        ("Type 3", "Type 3"),
    ]

    BODY_PART_OPTIONS = [
        ("Abdomen", "Abdomen"),
        ("Chest", "Chest"),
        ("Scul", "Scul"),
    ]

    DATA_DELIVERY = [("Kaapana", "Kaapana"), ("Raw data", "Raw data")]

    PATIENT_SEX = [
        ("Both male and female", "Both male and female"),
        ("Female", "Female"),
        ("Male", "Male"),
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
