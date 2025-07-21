"""
Amenity model definition and validation logic.

This module defines the Amenity class, which inherits from BaseModel.
Each amenity represents a feature or equipment offered by a place 
(e.g., Wi-Fi, parking, pool).

Core functionalities:
- Field validation for the amenity name (non-empty, max 50 characters)
- Many-to-many relationship with the Place model
- Update logic with validation
- Dictionary serialization for API use

The Amenity model is associated with places through the `place_amenity` 
association table and ensures consistent formatting of amenity data 
through validation.

Used libraries:
- SQLAlchemy for ORM and validation
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
