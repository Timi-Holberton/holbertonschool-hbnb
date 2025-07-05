#!/usr/bin/env python3

"""
Module defining the Amenity class.

This class represents an amenity or service available with a validated name
and methods for updating and converting to a dictionary.

It inherits from the BaseModel class which provides a unique identifier and common functionalities.

Main features:
- Strict validation of the name (type, presence, max length 50).
- Secure attribute updating via the update() method.
- Conversion to dictionary via to_dict() to facilitate serialization.

Exceptions are raised for invalid data to ensure the integrity of Amenity objects.
"""

from app.models.BaseModel import BaseModel
from app.models.association_tables import place_amenity

from app import db
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    """ amenity class that contains simple data about a comment on equipment and how it will be validated """
    __tablename__ = 'amenities' # Purée on a oublier ca !!!! Pffff
    name = db.Column(db.String(50), nullable=False)

    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities')

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_amenity_name('name', name)

    @validates('name')
    def validate_amenity_name(self, _key, name):
        """ Validate the name of the amenity """
        if not isinstance(name, str):
            raise ValueError(
                "Amenity name must be a string")
        if name == "":
            raise ValueError("Amenity name is required")
        if len(name) > 50:
            raise ValueError(
                "Amenity name must not exceed 50 characters")
        return name

    def update(self, data):
        """ update a amenity """
        # Vérifie la présence de la clé 'name' dans data
        if 'name' in data:
            # Vérifie que la valeur associée à 'name' est une chaîne non vide après suppression des espaces
            if not isinstance(data['name'], str) or not data['name'].strip():
                # Si la validation échoue, lève une exception pour indiquer que le nom est invalide
                raise ValueError("Invalid amenity name")
            # Si la validation est ok, met à jour l'attribut 'name' sans espaces en début/fin grâce à strip
            self.name = data['name'].strip()

    def to_dict(self):
        """Convert the amenity object into a dictionary format"""
        return {'id': self.id, 'name': self.name}
