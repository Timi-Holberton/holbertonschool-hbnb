#!/usr/bin/env python3

from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_amenity_name(name)

    def validate_amenity_name(self, name):
        """ function for the amenity name """
        if not isinstance(name, str):
            raise ValueError(
                "Le nom de l'agrément doit être une chaîne de caractères")
        if name.strip() == "":
            raise ValueError("Le nom de l'agrément est requis")
        if len(name) > 50:
            raise ValueError(
                "Le nom de l'agrément ne doit pas dépasser 50 caractères")
        return name
