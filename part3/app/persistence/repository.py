"""
Defines an abstract base class and an in-memory implementation for a generic repository pattern.

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

Details:
- InMemoryRepository stores objects in a dictionary keyed by their 'id' attribute.
- The update method assumes the stored objects implement their own update(data) method.
- get_by_attribute enables lookup by arbitrary attribute, useful for searching without knowing the ID.

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
