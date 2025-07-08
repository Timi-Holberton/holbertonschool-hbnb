"""
Provides an abstract base class and a SQLAlchemy-based implementation
for a generic repository pattern in the HBnB application.

Classes:
- Repository (ABC): Abstract base class specifying the interface for a repository managing CRUD operations.
- InMemoryRepository: Concrete implementation of Repository that stores objects in memory using a dictionary.

Responsibilities:
- add(obj): Add a new object to the repository.
- get(obj_id): Retrieve an object by its unique identifier.
- get_all(): Return a list of all stored objects.
- update(obj_id, data): Update an existing object identified by obj_id with provided data.
- delete(obj_id): Remove an object by its identifier.
- get_by_attribute(attr_name, attr_value): Retrieve an object matching a specific attribute value.

Implementation Notes:
- SQLAlchemyRepository expects that each model has a primary key named 'id'.
- The update method uses setattr and assumes model instances can be updated dynamically.
- get_by_attribute enables flexible filtering without knowing the object's ID.

This design abstracts persistence mechanisms and enables easy swapping or extension with other storage backends.
"""

from abc import ABC, abstractmethod
from app.models import User, Place, Review, Amenity  # Import your models
from app.models.user import User
from app import db
# from app.persistence import InMemoryRepository



# from app import db  # Assuming you have set up SQLAlchemy in your Flask app

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass



class SQLAlchemyRepository(Repository):
    """
    A generic repository class for performing CRUD operations using SQLAlchemy.

    This class provides a reusable implementation of the Repository pattern
    for any SQLAlchemy model. It abstracts common database interactions such as
    adding, retrieving, updating, and deleting records, and supports filtering by attributes.

    Attributes:
        model: The SQLAlchemy model class this repository manages.

    Methods:
        add(obj): Adds a new record to the database.
        get(obj_id): Retrieves a record by its primary key.
        get_all(): Retrieves all records for the model.
        update(obj_id, data): Updates a record with new data.
        delete(obj_id): Deletes a record by its ID.
        get_by_attribute(attr_name, attr_value): Finds a record by a specific attribute's value.
    """
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        from app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
