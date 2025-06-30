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


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}
        # dictionnaire pour stocker des objets avec comme clé leur id

    def add(self, obj):
        self._storage[obj.id] = obj
        # On a joute l'objet à storage en utilisant obj.id comme clé

    def get(self, obj_id):
        return self._storage.get(obj_id)
        # retourner l'objet à partir de son identifiant

    def get_all(self):
        return list(self._storage.values())
        # retourner tous les objets stockés en format de liste

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
    # on récupère les objets existants. On appelé la méthode update(data)
    # donc les objets doivent aussi avoir une méthode update
    # la classe user devra donc contenir cette méthode pour que
    # l'utilisateur puisse mettre à jour ses informations

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            # supprime l'objet avec l'identifiant donné

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
        # on veux récupérer un utilisateur dont l’email est par ex "alice@gmail.com" sans connaître son identifiant.
        # la méthode va regarder tous les objets stockés et retournerle premier utilisateur dont
        # l'attribut email correspond à "alice@gmail.com"

# from app import db  # Assuming you have set up SQLAlchemy in your Flask app

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
