from enum import Enum
from typing import List


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class ProjectStatus(ExtendedEnum):
    ETHICAL_APPROVAL = "Waiting for ethical approval"
    ETHICAL_APPROVAL_DENIED = "Ethical approval denied"
    ETHICAL_APPROVAL_APPROVED = "Ethical approval approved"
    RETRIEVING_DATA = "Retrieving data"
    UPLOADING_DATA = "Uplaoding data"
    UPLOADED = "Uploaded"


class PseudonymisaiontTypes(ExtendedEnum):
    NO_PESUDO = "No pseudonymisation"
    TYPE1 = "Type 1"
    TYPE2 = "Type 2"


class PatientGender(ExtendedEnum):
    MALE = "Male"
    FEMALE = "Female"
    BOTH = "Both"


OPTIONAL_EXAMIANTION_FORM_FIELDS: List = [
    "min_patient_age",
    "max_patient_age",
    "remittent",
    "producing_department",
    "modality_lab",
    "radiology_verdict",
]
