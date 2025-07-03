#!/usr/bin/env python3

"""
Module defining the BaseModel class.

This class serves as a base for other data models by providing
a unique identifier (UUID), creation and update timestamps,
as well as methods to save (update the modification date)
and dynamically update an instance's attributes.

Main features:
- Automatic generation of a UUID identifier as a string.
- Management of creation (`created_at`) and update (`updated_at`) dates.
- `save()` method to refresh the update timestamp.
- `update(data)` method to update attributes from a dictionary.
- Identifier validation via `valid_place_id()`.

Exceptions are raised to ensure data integrity.
"""

from app import db
import uuid
from datetime import datetime, UTC # Pour les fuseaux horaires



class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)) #)
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def valid_place_id(self):
        """ Ensure that the object's ID is a valid non-empty string """
        if not isinstance(self.id, str):
            raise ValueError(
                "The ID must be a string")
        if self.id.strip() == "":
            raise ValueError("The ID cannot be empty")
