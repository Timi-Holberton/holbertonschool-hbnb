"""
Package app.models

This package contains all the database models for the application.

The models are imported here to centralize their access and
to help prevent circular import issues between model modules.

By importing models in this __init__.py, other parts of the
application can import models directly from app.models, e.g.:

    from app.models import User, Place, Review, Amenity

This approach improves code organization and avoids import cycles.
"""

# app/models/__init__.py
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
