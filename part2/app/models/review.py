#!/usr/bin/env python3
from app.models.BaseModel import BaseModel


class Review(BaseModel):
    """Class Review with text, rating, user and place"""

    def __init__(self, text, rating, user, place):
        """ initiate the constructor"""
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user = self.validate_user(user)
        self.place = self.validate_place(place)

    def validate_text(self, text):
        """ condition to valide the text"""
        if not isinstance(text, str):
            raise ValueError(
                "The comment must be a string of characters.")
        if len(text) > 400:
            raise ValueError(
                "The comment must not exceed 400 characters.")
        return text

    def validate_rating(self, rating):
        """ Validate that a rating is an integer between 1 and 5 """
        if not isinstance(rating, int):
            raise ValueError("The rating must be a integer")
        if not 1 <= rating <= 5:
            raise ValueError("The rating must be between 1 and 5")
        return rating

    def validate_user(self, user):
        """ 
        Validate that the object passed as a parameter is indeed an instance 
        of the User model, to ensure that only valid entities are used in the code.
        """
        from app.models.user import User
        if not isinstance(user, User):
            raise TypeError("The user must be an instance of User.")
        return user

    def validate_place(self, place):
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
