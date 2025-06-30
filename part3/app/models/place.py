#!/usr/bin/env python3

"""
Module defining the Place class.

This class represents a place with its main attributes: title, description, price, 
geographical coordinates (latitude, longitude), owner, as well as its relationships 
with reviews and amenities.

The class includes strict validations for each attribute, 
methods to add reviews and amenities, 
and authorization checks related to the owner.

Main features:
- Validation of data (title, description, price, latitude, longitude).
- Management of relationships with reviews and amenities.
- User permission control for modifications.
- Conversion to dictionary for API serialization.

Exceptions are raised to ensure data integrity and modification security.
"""


from app.models.BaseModel import BaseModel


class Place(BaseModel):
    """ Classe Place who contains all of exception and the information about this"""
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """ constructor to declare all the attributes necessary"""
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
        if price < 0:
            raise ValueError("The price must be superior than 0")
        return price

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

    def validate_title(self, title):
        """ Validate the title of the place """
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if title.strip() == "":
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title

    def validate_description(self, description):
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

    def validate_owner(self, user):
        """Validate that the owner is a proper User instance"""
        from .user import User
        if not isinstance(user, User):
            raise ValueError("Owner must be an instance of User")
        if not hasattr(user, 'id') or not user.id:
            raise ValueError(
                "Owner must have a valid ID")
        return user  # qu'on assignera ensuite à self.owner

    def check_owner_permission(self, user):
        """Check if a user has permission to modify this place"""
        from .user import User
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User")
        if not hasattr(user, 'id') or not user.id:
            raise ValueError("User must have a valid ID")
        if self.owner.id != user.id:
            raise PermissionError(
                "You are not authorized to modify this place")

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
            'amenities': [a.to_dict() for a in self.amenities if hasattr(a, 'to_dict')]
        }
