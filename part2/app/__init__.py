from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns


# tu transformes ton app flask en API REST documentée

def create_app():
    """ function who Create and configure the Flask application with the RESTX API. """

    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')
    # Api(app) : lie l'instance api à Flask_restx.
    # Version de ton API
    # en clair : Cette ligne initialise ton API REST, la connecte à ton app Flask,
    # et active automatiquement une doc Swagger à l’URL /api/v1/.

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    return app
# ce code enregistre l'espace de noms des utilisateur, ce qui permet aux routes
# définies dans api/v1/users.py d'être accessibls via/api/v1/users
