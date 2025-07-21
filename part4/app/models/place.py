#!/usr/bin/env python3

"""
Module defining the Place class using SQLAlchemy ORM.

This class represents a place entity stored in a relational database, with
attributes such as title, description, price, geographical coordinates (latitude and longitude),
and owner reference. It manages relationships with other entities like reviews and amenities.

Key features include:
- Definition of database table columns and constraints via SQLAlchemy.
- Validation of attribute data using SQLAlchemy's @validates decorator and property setters.
- Relationship management to related tables/models (User, Review, Amenity) with back_populates.
- Enforcement of uniqueness constraints at the database level (e.g., unique title per owner).
- Methods for adding related objects while ensuring type safety.
- Permission checks based on owner ownership.
- Serialization of the Place instance to a dictionary, including related objects, for API responses.

This design leverages SQLAlchemy ORM capabilities to ensure data integrity, 
manage relationships efficiently, and provide a clear mapping between Python objects and database tables.
"""

from app.models.BaseModel import BaseModel
from app.models.association_tables import place_amenity
from app import db
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint # pour utiliser des contraintes pour empêcher doublons


class Place(BaseModel):
    """ Classe Place who contains all of exception and the information about this"""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(4000), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', back_populates='places')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')
    reviews = db.relationship('Review', back_populates='place', lazy=True, cascade='all, delete-orphan')

##---------------------------------------------------------------------------##
##---------------------------------------------------------------------------##
    __table_args__ = (
        UniqueConstraint('title', 'owner_id', name='unique_place_title_owner'),
    )
    # __table_args__ doit être soit un tuple ou un dictionnaire.
    # crée une contrainte d’unicité sur une ou plusieurs colonnes dans la base de données.
    # Cela signifie que la base refusera l’insertion d’une ligne si la combinaison
    # des valeurs de title et de l'owner existe déjà.
    # La combinaison de title et owner doit être unique sinon erreur
##---------------------------------------------------------------------------##
##---------------------------------------------------------------------------##
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """ constructor to declare all the attributes necessary"""
        super().__init__()
        self.title = self.validate_title('title', title)
        self.description = self.validate_description('description', description)
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @validates('title')
    def validate_title(self, _key, title):
        """ Validate the title of the place """
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if title.strip() == "":
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title

    @validates('description')
    def validate_description(self, _key, description):
        """ Validate the description of the place """
        if description is not None:
            if not isinstance(description, str):
                raise ValueError(
                    "Description must be a string")
            if description.strip() == "":
                raise ValueError("Description is required")
            if len(description) > 4000:
                raise ValueError("Description must not exceed 4000 characters")
        return description

    @property
    def price(self):
        """ return the stored price """
        return self._price

    @price.setter
    def price(self, price):
        """ validate price before setting it"""
        self._price = self.validate_price(price)

    def validate_price(self, price):
        """ function price for the place"""
        if not isinstance(price, (int, float)):
            raise ValueError("The price must be a number")
        if price <= 0:
            raise ValueError("The price must be superior than 0")
        return price

    @property
    def latitude(self):
        """ Returns the stored latitude """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """ Validates latitude before setting it """
        self._latitude = self.validate_latitude(latitude)

    def validate_latitude(self, latitude):
        """ check for the latitude """
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if not -90.0 <= latitude <= 90.0:
            raise ValueError(
                "Latitude must be between -90.0 and 90.0")
        return latitude

    @property
    def longitude(self):
        """ returns the stored latitude """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """ validate longitude before setting it"""
        self._longitude = self.validate_longitude(longitude)

    def validate_longitude(self, longitude):
        """ check for the longitude """
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError(
                "Longitude must be between -180 and 180 °C")
        return longitude

    @validates('owner_id')
    def validate_owner_id(self, _key, owner_id):
        # Ici, tu peux valider le format UUID, par exemple (import uuid)
        import uuid
        try:
            uuid.UUID(str(owner_id))
        except ValueError:
            raise ValueError("owner_id must be a valid UUID string")
        return owner_id

    def check_owner_permission(self, user):
        """Check if a user has permission to modify this place"""
        from .user import User
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User")
        if not hasattr(user, 'id') or not user.id:
            raise ValueError("User must have a valid ID")
        if self.owner_id != user.id:
            raise PermissionError(
                "You are not authorized to modify this place")

    def add_review(self, review):
        """ Add a review to the place """
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected argument 'review' to "
                            "be an instance of Review.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """ Add an amenity to the place """
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected argument 'amenity' to "
                            "be an instance of Amenity.")
        self.amenities.append(amenity)

    def to_dict(self):
        """ Convert this Place object to a dictionary (used for API responses) """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [a.to_dict() for a in self.amenities if hasattr(a, 'to_dict')],
            'reviews': [review.to_dict() for review in self.reviews]
        }
