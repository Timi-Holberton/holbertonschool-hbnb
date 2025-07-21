"""
Review model definition and validation logic.

This module defines the Review class, which inherits from BaseModel.
A review is associated with a user and a place, and contains a comment (text)
and a numerical rating (1 to 5). 

Core functionalities:
- Field validation for text, rating, user_id, and place_id
- ORM relationships to User and Place models
- Dictionary serialization for API output

Each review is linked to:
- A user (via user_id)
- A place (via place_id)

This model ensures strong data integrity and enforces constraints 
on comment length, rating range, and UUID formatting.

Used libraries:
- SQLAlchemy for ORM and validation
"""

from app.models.BaseModel import BaseModel
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Review class with text, rating, user_id and place_id UUID references."""
    __tablename__ = 'reviews'

    # Colonne contenant le texte du commentaire (400 caractères max, obligatoire)
    text = db.Column(db.String(400), nullable=False)
    # Colonne contenant la note (entier entre 1 et 5, obligatoire)
    rating = db.Column(db.Integer, nullable=False)
    # Clé étrangère vers l'id de l'utilisateur (UUID sous forme de string, obligatoire)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # Clé étrangère vers l'id du lieu (UUID sous forme de string, obligatoire)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relation ORM vers l'objet User, pour accéder aux données utilisateur liées
    user = db.relationship('User', back_populates='reviews')
    # Relation ORM vers l'objet Place, pour accéder aux données lieu liées
    place = db.relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, user_id, place_id):
        """Initialize a Review instance with text, rating, user_id and place_id."""
        super().__init__()
        self.text = self.validate_text("text", text)
        self.rating = self.validate_rating("rating", rating)
        self.user_id = self.validate_user_id("user_id", user_id)
        self.place_id = self.validate_place_id("place_id", place_id)

    @validates('text')
    def validate_text(self, _key, text):
        """Validate that text is a non-empty string with max length 400."""
        if not isinstance(text, str):
            raise ValueError("The comment must be a string.")
        if not text:
            raise ValueError("Text is required.")
        if len(text) > 400:
            raise ValueError("The comment must not exceed 400 characters.")
        return text

    @validates('rating')
    def validate_rating(self, _key, rating):
        """Validate that rating is an integer between 1 and 5."""
        if not isinstance(rating, int):
            raise ValueError("The rating must be an integer.")
        if not 1 <= rating <= 5:
            raise ValueError("The rating must be between 1 and 5.")
        return rating

    @validates('user_id')
    def validate_user_id(self, _key, user_id):
        """Validate that user_id is a 36-character UUID string."""
        if not isinstance(user_id, str):
            raise ValueError("user_id must be a UUID string.")
        if len(user_id) != 36:
            raise ValueError("user_id must be 36 characters long (UUID format).")
        return user_id

    @validates('place_id')
    def validate_place_id(self, _key, place_id):
        """Validate that place_id is a 36-character UUID string."""
        if not isinstance(place_id, str):
            raise ValueError("place_id must be a UUID string.")
        if len(place_id) != 36:
            raise ValueError("place_id must be 36 characters long (UUID format).")
        return place_id

    def to_dict(self):
        """Convert the Review instance to a Python dictionary for serialization."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
