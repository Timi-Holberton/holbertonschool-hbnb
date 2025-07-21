
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):
    """
    Create and configure the Flask application instance.

    This factory function initializes the Flask app with the specified configuration class.
    It sets up extensions including JWTManager, Bcrypt for password hashing, and SQLAlchemy for ORM.
    Additionally, it registers the API namespaces for users, places, amenities, reviews, and authentication,
    organizing the application routes under the versioned API prefix.

    Args:
        config_class (str): The configuration class to use for the app settings (default: 'config.DevelopmentConfig').

    Returns:
        Flask: The fully configured Flask application instance ready to run.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    from app.models.user import User
    from app.models.place import Place
    from app.models.amenity import Amenity
    from app.models.review import Review
    from app.models.association_tables import place_amenity


    # Déclaration de la sécurité Swagger (JWT token dans l'en-tête Authorization)
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Exemple : Bearer <votre_token>'
        }
    }

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',  # Swagger UI accessible ici
        authorizations=authorizations,
        security='Bearer Auth'  # Appliqué par défaut à toutes les routes (sauf si on override)
    )

    # Importation et enregistrement des namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    #Crée toutes les tables en base si elles n’existent pas déjà.
    with app.app_context():
        db.create_all()

    return app
