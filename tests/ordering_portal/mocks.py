from project.orderingportal.forms import LoginForm
from project.orderingportal.models import User


class MockStore:
    """Mock the store class."""

    def login(form: LoginForm) -> bool:
        """Login in a user without a http request"""

        user: User = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            return True

        return False
