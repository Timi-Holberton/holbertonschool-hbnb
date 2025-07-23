
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=config.DevelopmentConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, supports_credentials=True, origins=["http://localhost:8000"])

    # Désactive la distinction entre URLs avec ou sans slash final
    # Permet d'éviter les redirections 308/301 qui posent problème
    # notamment lors des requêtes CORS préflight OPTIONS
    app.url_map.strict_slashes = False

    jwt.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    @app.route('/')
    def index():
        return 'Bienvenue sur l’API HBnB. Swagger est à /api/v1/'

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
