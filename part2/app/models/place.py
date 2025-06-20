#!/usr/bin/env python3
from app.models.BaseModel import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = self.validate_description(description)
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = self.validate_price(price)

    def validate_price(self, price):
        """ function price for the place"""
        if not isinstance(price, (int, float)):
            raise ValueError("Le prix doit être un nombre")
        if price < 0:
            raise ValueError("Le prix doit être supérieur à 0")
        return price

    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, longitude):
        self._longitude = self.validate_longitude(longitude)

    def validate_longitude(self, longitude):
        if not isinstance(longitude, (int, float)):
            raise ValueError("La longitude doit être un nombre")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError(
                "La longitude doit être comprise entre -180 et 180 °C")
        return longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = self.validate_latitude(latitude)

    def validate_latitude(self, latitude):
        if not isinstance(latitude, (int, float)):
            raise ValueError("La latitude doit être un nombre")
        if not -90.0 <= latitude <= 90.0:
            raise ValueError(
                "La latitude doit être comprise entre -90.0 et 90.0")
        return latitude

    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected argument 'review' to "
                            "be an instance of Review.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected argument 'amenity' to "
                            "be an instance of Amenity.")
        self.amenities.append(amenity)

    def validate_title(self, title):
        """ function title for the place"""
        if not isinstance(title, str):
            raise ValueError("Ce n'est pas une chaîne de caractères")
        if len(title) > 100:
            raise ValueError("Il y a trop de caractères (maximum 100)")
        return title

    def validate_description(self, description):
        """ function description for the place"""
        if description is not None:
            if not isinstance(description, str):
                raise ValueError(
                    "La description doit être une chaîne de caractères")
            if len(description) > 4000:
                raise ValueError("Pas plus de 4000 caractères !!")
        return description

    def validate_owner(self, user):
        from .user import User
        """Vérifie que User est un propriétaire acceptable pour le lieu"""
        if not isinstance(user, User):
            raise ValueError("Le propriétaire doit être une instance de User")
        if not hasattr(user, 'id') or not user.id:
            raise ValueError(
                "Le propriétaire doit avoir un identifiant valide")
        return user  # qu'on assignera ensuite à self.owner

    def check_owner_permission(self, user):
        """Vérifie que l'utilisateur est autorisé à modifier ce lieu"""
        from .user import User
        if not isinstance(user, User):
            raise ValueError("L'utilisateur doit être une instance de User")
        if not hasattr(user, 'id') or not user.id:
            raise ValueError("L'utilisateur doit avoir un identifiant valide")
        if self.owner.id != user.id:
            raise PermissionError(
                "Vous n'êtes pas autorisé à modifier ce lieu")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [a.to_dict() for a in self.amenities if hasattr(a, 'to_dict')]
        }
