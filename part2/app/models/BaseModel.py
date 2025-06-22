#!/usr/bin/env python3

import uuid
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
# nous stockons le UUIDgénéré sous forme de fichier a String pour éviter les
# problèmes lors de la récupération à partir du référentiel de mémoire.
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
