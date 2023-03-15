"""Ordering Portal exceptions."""


class OrderingPoratalError(Exception):
    """Base expeception for the package"""

    def __init__(self, message: str = ""):
        super().__init__(message)


class ProjectFormError(OrderingPoratalError):
    """Exception raised when a project form is not valid."""


class ExaminationFormError(OrderingPoratalError):
    """Exception raised when a examination form is not valid."""
