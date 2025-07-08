from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """
    Repository class for managing User entities using SQLAlchemy.

    This class extends the generic SQLAlchemyRepository to provide
    additional query methods specific to the User model, such as
    retrieving a user by their email address.

    Methods:
        get_user_by_email(email): Returns the first user found with the given email.
    """
    def __init__(self):
        """ Initializes the UserRepository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """ Retrieve a user instance by their email address."""
        return self.model.query.filter_by(email=email).first()
