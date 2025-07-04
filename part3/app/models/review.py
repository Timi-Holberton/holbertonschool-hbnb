#!/usr/bin/env python3

"""
Module defining the Review class.

This class represents a review left by a user on a place, with text
and a rating between 1 and 5. It strictly validates each attribute's data
and ensures consistency in the relationships between the user and the place.

Main features:
- Validation of the text (type and maximum length).
- Validation of the rating (integer between 1 and 5).
- Validation that the user is a valid instance of the User class.
- Validation that the place is a valid instance of the Place class.
- Conversion of the object to a dictionary for serialization.

Exceptions are raised to ensure the robustness and integrity of Review objects.
"""



from app.models.BaseModel import BaseModel
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Class Review with text, rating, user and place"""
    __tablename__ = 'reviews'

    text = db.Column(db.String(400), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    """
        
        user = db.relationship('User', backref='reviews')
    Cette ligne crée une relation ORM entre Review et User.
    Grâce à ça :

    Depuis un objet Review, tu peux accéder à review.user pour récupérer l'utilisateur qui a écrit l’avis.

    Depuis un objet User, tu peux accéder à user.reviews pour voir tous les avis
    laissés par cet utilisateur (grâce au backref).
        
        place = db.relationship('Place', backref='reviews')
    """
    def __init__(self, text, rating, user, place):
        """ initiate the constructor"""
        super().__init__()
        self.text = self.validate_text("text", text)
        self.rating = self.validate_rating("rating", rating)
        self.user = self.validate_user("user_id", user)
        self.place = self.validate_place("place_id", place)

    @validates('text')
    def validate_text(self, _key, text):
        """ condition to valide the text"""
        if not isinstance(text, str):
            raise ValueError(
                "The comment must be a string of characters.")
        if not text:
            raise ValueError("text is required")

        if len(text) > 400:
            raise ValueError(
                "The comment must not exceed 400 characters.")
        return text

    @validates('rating')
    def validate_rating(self, _key, rating):
        """ Validate that a rating is an integer between 1 and 5 """
        if not isinstance(rating, int):
            raise ValueError("The rating must be a integer")
        if not 1 <= rating <= 5:
            raise ValueError("The rating must be between 1 and 5")
        return rating

    @validates('user_id')
    def validate_user(self, _key, user):
        """ 
        Validate that the object passed as a parameter is indeed an instance 
        of the User model, to ensure that only valid entities are used in the code.
        """
        from app.models.user import User
        if not isinstance(user, User):
            raise TypeError("The user must be an instance of User.")
        return user

    @validates('place_id')
    def validate_place(self, _key, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("The location must be an instance of Place.")
        return place

    def to_dict(self):
        """ This method converts a Review instance into a Python dictionary,"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None
        }
