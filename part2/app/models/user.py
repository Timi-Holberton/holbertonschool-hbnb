#!/usr/bin/env python3
from email_validator import validate_email, EmailNotValidError
from app.models.BaseModel import BaseModel
import re
"""
class User : hérite de BaseModel.
methode : validation des données et exigeances
Cardinalité : User peut posséder plusieurs Place
"""


class User(BaseModel):
    """
    Class User : hérite de BaseModel.
    methode : validation des données et exigeances
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Récupère id, created_at et update_at de la class BaseModel
        Initialise first_name, last_name, email, is_admin avec
        des méthodes de validation
        """
        super().__init__()
        self.first_name = self.validate_name(first_name, "first_name")
        self.last_name = self.validate_name(last_name, "last_name")
        self.email = self.validate_email(email)
        # self.__password_hashé = self.validate_password(password)
        self.is_admin = self.validate_is_admin(is_admin)
        self.places = []  # Liste pour stocker les Hébergements liés
        self.reviews = []  # Liste pour stocker les avis liés

    def validate_name(self, name, field="Name"):
        if not isinstance(name, str):
            raise ValueError(f"{field} doit être une chaîne de caractères.")
        name = name.strip()
        if not name:
            raise ValueError(
                f"{field} non valide, veuillez entrer des caractères.")
        if not (1 <= len(name) <= 50):
            raise ValueError(
                f"{field} doit contenir entre 1 et 50 caractères.")
        if not re.match("^[a-zA-ZÀ-ÿ-]+$", name):
            raise ValueError(
                f"{field} ne doit contenir que des lettres ou des traits d’union.")
        return name

    def validate_email(self, email):
        """
        Méthode de validation qui vérifie si l'email est valide
        en utilisant la librairie email-validator (requirement)
        """
        try:
            validate = validate_email(email)
            # on appelle la bibliothèque validate_email et on la valide
            return validate.email
        # si l'email est valide il renvoie l'email(en version propre)
        except EmailNotValidError as email_error:
            raise ValueError(f"Erreur email invalide : {email_error}")

    def validate_is_admin(self, is_admin):
        """
        Méthode de validation qui vérifie si l'utilisateur est un admin
        ou non, par défaut = False
        """
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin doit être un booléen")
        return is_admin

    def add_review(self, review):
        # sert à vérifier que l’objet passé est bien un Review.
        # empêche d'ajouter des types inattendus.
        # La liste reviews ne contient que des objets Review.
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected argument 'review' to "
                            "be an instance of Review.")
        self.reviews.append(review)

    def add_place(self, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Expected argument 'place' to "
                            "be an instance of Place.")
        self.places.append(place)

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, }
