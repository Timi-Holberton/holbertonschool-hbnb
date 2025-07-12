"""
User model definition and data validation logic.

This module defines the User class, which inherits from BaseModel.
It includes fields such as first_name, last_name, email, password, and is_admin.
The model manages relationships with Place and Review models, ensuring data integrity.

Core functionalities:
- Field validation (name, email, admin flag)
- Password hashing and verification
- Relationship management with places and reviews
- Conversion to dictionary for serialization
- Update method with strict validation on sensitive fields

Libraries used:
- SQLAlchemy for ORM mapping
- email_validator for email validation
- bcrypt (via Flask-Bcrypt) for secure password hashing

This model enforces data quality and supports secure user management
in the HBnB application backend.
"""

from email_validator import validate_email, EmailNotValidError
from app.models.BaseModel import BaseModel
import re
from flask_bcrypt import Bcrypt
from app import db
from sqlalchemy.orm import validates

# from app.extensions import db

bcrypt = Bcrypt()

class User(BaseModel):
    """
    Class User: inherits from BaseModel.
    Method: data validation and requirements
    """
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relation avec les lieux (places) que l’utilisateur possède
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')

    # Relation avec les avis (reviews) que l’utilisateur a rédigés
    reviews = db.relationship('Review', back_populates='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Retrieve id, created_at, and update_at from the BaseModel class.
        Initialise first_name, last_name, email, and is_admin with
        validation methods.
        """
        super().__init__()
        # attention avec l'utilisation des décorateurs validates, la position
        # des arguments pour first_name + last_name + is_admin à changer avec
        # l'ajout de l'argument key
        self.first_name = self.validate_name("first_name", first_name)
        self.last_name = self.validate_name("last_name", last_name)
        self.email = email
        self.hash_password(password)
        self.is_admin = self.validate_is_admin("is_admin", is_admin)
        self.places = []  # Liste pour stocker les Hébergements liés
        self.reviews = []  # Liste pour stocker les avis liés

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """ function that manages the validation conditions for the first name """
        if not isinstance(name, str):
            raise ValueError(f"{key} must be a string.")
        name = name.strip()
        if not name:
            raise ValueError(
                f"{key} Invalid, please enter characters.")

        if not (1 <= len(name) <= 50):
            raise ValueError(
                f"{key} must contain between 1 and 50 characters.")
        if not re.fullmatch(r"[ a-zA-ZÀ-ÿ-]+", name):
            raise ValueError(
                f"{key} must contain only letters or hyphens.")
        return name

    @validates('email')
    def validation_e_mail(self, _key, email):
        """
        Validation method that checks whether the email address is valid
        using the email-validator library (requirement)
        """
        try:
            valid = validate_email(email)
            # on appelle la bibliothèque validate_email et on la valide
            return valid.normalized
        # si l'email est valide il renvoie l'email(en version propre)
        except EmailNotValidError as email_error:
            raise ValueError(f"Error, invalid email : {email_error}")

    @validates('is_admin')
    def validate_is_admin(self, _key, is_admin):
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
            self.email = self.validation_e_mail(data['email'])

        # Si la clé 'first_name' est présente dans les données reçues
        if 'first_name' in data:
            # On valide et met à jour le prénom via la méthode validate_name
            self.first_name = self.validate_name("first_name", data['first_name'])

        # Si la clé 'last_name' est présente dans les données reçues
        if 'last_name' in data:
            # On valide et met à jour le nom de famille via la méthode validate_name
            self.last_name = self.validate_name("last_name", data['last_name'])

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
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'reviews': [review.to_dict() for review in self.reviews],
            'places': [place.to_dict() for place in self.places]
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
