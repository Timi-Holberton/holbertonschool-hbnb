#!/usr/bin/env python3
from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """ Class Review who contains a text, a note. user and place need to
    use this class Review """

    def __init__(self, text, rating, user, place):
        """ constructor of the class Review """
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.user = self.validate_user(user)
        self.place = self.validate_place(place)

    def validate_rating(self):
        """ error condition for rating review """
        if not isinstance(self.rating, int):
            raise ValueError("Ce n'est pas un entier")
        if not 1 <= self.rating <= 5:
            raise ValueError("review must be between 1 and 5")

    def validate_text(self):
        """  error condition for text review """
        if not isinstance(self.text, str):
            raise ValueError("Ce n'est pas du texte")
        if len(self.text) > 400:
            raise ValueError("Ne dépasser pas 400 caractères")

    def validate_place(self):
        """ error condition for validate place in the class review"""
        if not isinstance(self.place, Place):
            raise TypeError("Le lieu doit être une instance de Place")

    def validate_user(self):
        """ error condition for validate user in the class review"""
        if not isinstance(self.user, User):
            raise TypeError("L'utilisateur doit être une instance de User")
