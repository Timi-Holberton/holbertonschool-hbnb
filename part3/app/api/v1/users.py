"""
User management module via a RESTful API using Flask-RESTx.

This module defines a Flask-RESTx namespace dedicated to user-related operations,
providing endpoints to create, retrieve, and update users registered in the application.

Main functionalities:
- POST /users/               : Create a new user.
- GET /users/                : Retrieve the list of all users.
- GET /users/<user_id>       : Retrieve a user by their ID.
- PUT /users/<user_id>       : Update user information (authenticated users can update only their own data).

Each endpoint uses Flask-RESTx models for input validation
and automatic API documentation via Swagger.

Operations rely on the 'facade' service to handle business logic
and data access, including checking email uniqueness.

Security:
- JWT authentication is required for updating user information.
- Users cannot change their email or password through the update endpoint.

HTTP status codes used:
- 200 : Successful operation.
- 201 : Resource successfully created.
- 400 : Invalid input data or email already registered.
- 403 : Unauthorized action.
- 404 : User not found.

This module enforces strict input validation
(first name, last name, email) and provides interactive documentation via Swagger UI.
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

# Namespace : permet de créer des groupe logique d'url et de ressources pour API
# Ressource : Classe de base pour définir les point de terminaison (endpoints) d'une API REST
# Fields :Sert à donner les modèles données pour la validation et la doc Swagger


# crée un sous-ensemble d'URL, ici pour les utilisateur (/users)
# Swagger générera une sectoin"user operations"
api = Namespace('users', description='User operations')

# Définir le modèle utilisateur pour la validation et la documentation des entrées
# api.model: défini un schéma JSON pour les entrées utilisateur (Swagger)
# chaque champ est requis puisque required=True, etdoit avoir une descritpion
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Administrator status')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Administrator status'),
})


@api.route('/')
# Déclare une 'ressource' (hérite de Ressource) attaché à la route /users/
# gère les requêtes HTTP POST
class UserList(Resource):
    # @api.expect :indique que la requête doit contenir un JSON conforme à 'user_model'
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    @api.doc(description="Register a new user")
    def post(self):
        """Register a new user"""
        # api.payload : Récupère le corps JSONde la requête sous forme de dico

        user_data = api.payload

        # Simuler la vérification de l'unicité des e-mails (à remplacer par une véritable validation avec persistance)
        # Appelle 'facade.get_user_by_email()' pour vérifier si l'email est déjà utilisé
        # si oui, retourne une erreur 400 avec message explicite
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        # Appelle 'facade.create_user()' pour enregistrer le nouvel utilisateur en base
        try:
            new_user = facade.create_user(user_data)
        except ValueError as error :
            return {'error': str(error)}, 400
        # Retourne les info du nouvel utilisateur avec un code 201 ("created")
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin': new_user.is_admin
            # 'password': new_user.password ne jamais l'affiché
            }, 201

        # Résumé du code :
        # Valide automatiquement les données avec le modèleSwagger
        # Vérifie si l'email est déjà utilisé
        # Créer l'utilisateur si tout es OK
        # Fournit une doc interactive avec SwaggerUI

        # Le code suivant définti un endpoint GET
        # pour récupérer les infos d'un utilisateur à partir de son ID

    @api.response(200, 'List of users retrieved')
    @api.response(404, 'No users found')
    @api.doc(description="Retrieve the list of all users")
    def get(self):
        """ return the lists of users """
        users = facade.get_all()
        return users, 200


@api.route('/<user_id>', methods=['GET', 'PUT'])
# créer une route de type /users/12345 par exemple, <user_id est une valeur dynamique extraite directement de l'URL
# la classe 'UserRessosurce' est lié à cette route et va gérer les requêtes comme GET, PUT, DELETE
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.doc(description="Get user details by ID")
    def get(self, user_id):
        """Get user details by ID"""
        # Appelle la méthode get_user du module facade, en lui passant l'ID demandé
        # cette fonction interroge la base de données ou la couche métier pour trouveerl'utilisateur correspondant
        user = facade.get_user(user_id)
        # Si l'utilisateur n'xiste pas (None ou équivalent) l'API retourne message d'erreur et code
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'reviews': [review.to_dict() for review in user.reviews],
            'places': [place.to_dict() for place in user.places]
        }, 200
        # si utilisateur est trouvé, l'API retoiurne ses données dans un dico JSON avec code
    @jwt_required()
    @api.doc(security='Bearer Auth', description="Update user details (user can update only own data, except email and password)")
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data or forbidden field modification')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        data = request.json
        if not data:
            return {"error": "Data not found"}, 400

        current_user = get_jwt_identity()

        if str(current_user["id"]) != str(user_id):
            return {'error': "Unauthorized action"}, 403

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Autoriser email si inchangés
        if ("email" in data and data["email"] != user.email):
            return {'error': "You cannot change your email adress"}, 400
        # Empêcher la modification de l’email ou du mot de passe
        if "password" in data:
            return {'error': "You cannot change your password"}, 400

        try:
            user = facade.update_user(user_id, data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is-admin': user.is_admin
        }, 200
