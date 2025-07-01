from flask import Flask
from flask_restx import Api
# from app import create_app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_jwt_extended import JWTManager

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
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

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    return app


