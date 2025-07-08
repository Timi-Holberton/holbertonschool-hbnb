"""
Association table for many-to-many relationship between Place and Amenity.

This module defines the `place_amenity` table, which connects the `places`
and `amenities` tables in a many-to-many relationship using SQLAlchemy's `db.Table`.

Each entry in this table represents a link between a specific Place and an Amenity.

Structure:
- place_id: Foreign key referencing the `places.id`, also part of the primary key.
- amenity_id: Foreign key referencing the `amenities.id`, also part of the primary key.

Used in the Place and Amenity models to enable bidirectional relationships.
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
