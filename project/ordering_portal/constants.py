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
    ]

    BODY_PART_OPTIONS = [
        ("Abdomen", "Abdomen"),
        ("Chest", "Chest"),
        ("Scul", "Scul"),
    ]
