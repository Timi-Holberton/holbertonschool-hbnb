#!/usr/bin/env python3

"""
Module defining the User class.

This class represents a user with personal information 
(first name, last name, email) and their administrator status. 
It includes rigorous validation methods to ensure data integrity, 
as well as methods to manage relationships with places and reviews associated with the user.

Main features:
- Validation of names (first and last) with rules on length and allowed characters.
- Email validation using the external email-validator library.
- Management of administrator status (boolean).
- Data updating with strict validation for sensitive fields.
- Association of Review and Place objects to the user.
- Conversion of the object to a dictionary for serialization.

Exceptions are raised to ensure validation robustness.
"""



from email_validator import validate_email, EmailNotValidError
from app.models.BaseModel import BaseModel
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    """
    Class User: inherits from BaseModel.
    Method: data validation and requirements
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Retrieve id, created_at, and update_at from the BaseModel class.
        Initialise first_name, last_name, email, and is_admin with
        validation methods.
        """
        super().__init__()
        self.first_name = self.validate_name(first_name, "first_name")
        self.last_name = self.validate_name(last_name, "last_name")
        self.email = self.validate_email(email)
        self.password = self.verify_password(password)
        self.is_admin = self.validate_is_admin(is_admin)
        self.places = []  # Liste pour stocker les Hébergements liés
        self.reviews = []  # Liste pour stocker les avis liés

    def validate_name(self, name, field="Name"):
        """ function that manages the validation conditions for the first name """
        if not isinstance(name, str):
            raise ValueError(f"{field} must be a string.")
        name = name.strip()
        if not name:
            raise ValueError(
                f"{field} Invalid, please enter characters.")
        if not (1 <= len(name) <= 50):
            raise ValueError(
                f"{field} must contain between 1 and 50 characters.")
        if not re.match("^[a-zA-ZÀ-ÿ-]+$", name):
            raise ValueError(
                f"{field} must contain only letters or hyphens.")
        return name

    def validate_email(self, email):
        """
        Validation method that checks whether the email address is valid
        using the email-validator library (requirement)
        """
        try:
            validate = validate_email(email)
            # on appelle la bibliothèque validate_email et on la valide
            return validate.normalized
        # si l'email est valide il renvoie l'email(en version propre)
        except EmailNotValidError as email_error:
            raise ValueError(f"Error, invalid email : {email_error}")

    def validate_is_admin(self, is_admin):
        """
        Validation method that checks whether the user is an admin
        or not, default = False
        """
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be an booleen")
        return is_admin

    def update(self, data):
        """ It applies strict validation to certain sensitive fields (email, first_name, last_name, is_admin). """
        # Si la clé 'email' est présente dans les données reçues
        if 'email' in data:
            # On utilise la méthode de validation d'email pour s'assurer que l'adresse est valide
            self.email = self.validate_email(data['email'])

        # Si la clé 'first_name' est présente dans les données reçues
        if 'first_name' in data:
            # On valide et met à jour le prénom via la méthode validate_name
            self.first_name = self.validate_name(data['first_name'], "first_name")

        # Si la clé 'last_name' est présente dans les données reçues
        if 'last_name' in data:
            # On valide et met à jour le nom de famille via la méthode validate_name
            self.last_name = self.validate_name(data['last_name'], "last_name")

        # Si la clé 'is_admin' est présente dans les données reçues
        if 'is_admin' in data:
            # On valide que c’est un booléen et on met à jour
            self.is_admin = self.validate_is_admin(data['is_admin'])

        # Pour toutes les autres clés présentes dans data (non listées ci-dessus)
        for key, value in data.items():
            # On ignore celles déjà traitées pour éviter d'écraser avec des valeurs non validées
            if key not in ['email', 'first_name', 'last_name', 'is_admin']:
                # Mise à jour directe de l’attribut sans validation supplémentaire
                setattr(self, key, value)

    def add_review(self, review):
        """ function that allows you to add a Review object to an internal list """
        # sert à vérifier que l’objet passé est bien un Review.
        # empêche d'ajouter des types inattendus.
        # La liste reviews ne contient que des objets Review.
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected argument 'review' to "
                            "be an instance of Review.")
        self.reviews.append(review)

    def add_place(self, place):
        """ It allows you to add a Place object to an internal list. """
        from app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Expected argument 'place' to "
                            "be an instance of Place.")
        self.places.append(place)

    def to_dict(self):
        """ Convert a user object (User) into a Python dictionary """
        # transforme une liste de user en dico
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
