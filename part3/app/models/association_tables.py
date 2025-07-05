"""
Defines the association table between places and amenities.

This module declares a many-to-many relationship between the Place and Amenity models
using a SQLAlchemy association table. Each entry in the table links one place to one amenity.

Main features:
- Enables multiple amenities to be associated with multiple places.
- Ensures uniqueness of each (place_id, amenity_id) pair using composite primary key.
"""
from app import db

# Table d'association pour la relation plusieurs-à-plusieurs entre Place et Amenity
place_amenity = db.Table(
    'place_amenity',  # Nom de la table dans la base de données

    # Clé étrangère vers la table 'places', avec contrainte de clé primaire
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),

    # Clé étrangère vers la table 'amenities', avec contrainte de clé primaire
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)
