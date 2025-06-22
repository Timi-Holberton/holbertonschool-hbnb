#!/usr/bin/env python3
from app.models.BaseModel import BaseModel


class Review(BaseModel):
    """Class Review with text, rating, user and place"""

    def __init__(self, text, rating, user, place):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user = self.validate_user(user)
        self.place = self.validate_place(place)

    def validate_text(self, text):
        if not isinstance(text, str):
            raise ValueError(
                "Le commentaire doit être une chaîne de caractères")
        if len(text) > 400:
            raise ValueError(
                "Le commentaire ne doit pas dépasser 400 caractères")
        return text

    def validate_rating(self, rating):
        if not isinstance(rating, int):
            raise ValueError("La note doit être un entier")
        if not 1 <= rating <= 5:
            raise ValueError("La note doit être comprise entre 1 et 5")
        return rating

    def validate_user(self, user):
        from app.models.user import User
        if not isinstance(user, User):
            raise TypeError("L'utilisateur doit être une instance de User")
        return user

    def validate_place(self, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Le lieu doit être une instance de Place")
        return place

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None
        }
