"""
Admin management module.

This module provides RESTful API endpoints for administrative operations
such as creating and updating users, amenities, and places.

Endpoints require JWT authentication and restrict access to users
with admin privileges where applicable.

Features include:
- Admin user creation and modification.
- Amenity creation and modification.
- Place modification accessible to admins or place owners.

All input data are validated using Flask-RESTx models and
appropriate HTTP status codes are returned to indicate success or errors.

The module relies on a facade service layer to encapsulate
business logic and data access.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from werkzeug.security import generate_password_hash
from app.services import facade

api = Namespace('admin', description='Admin operations')

user_model = api.model('admin', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Administrator status')
})

amenity_model = api.model('AmenityModel', {
    'name': fields.String(required=True, description='Name of the amenity')
})

place_update_model = api.model('admin_place_update', {
    'title': fields.String(description="Title of the place (max 100 characters)"),
    'description': fields.String(description="Description of the place (max 4000 characters)"),
    'price': fields.Float(description="Price per night, must be positive"),
    'latitude': fields.Float(description="Latitude between -90.0 and 90.0"),
    'longitude': fields.Float(description="Longitude between -180.0 and 180.0"),
    'amenities': fields.List(fields.String, description="List of amenity UUIDs to associate")
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)  # Active la validation automatique,
    @api.response(201, 'User_admin successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @api.doc(description="Register a new user (admin only)")
    def post(self):
        """
        Create a new user with admin privileges.
        """
        current_user = get_jwt_identity()
        # Vérification des droits d'administration
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Récupération et traitement des données entrantes
        user_data = request.json
        email = user_data.get('email')

        # Vérification unicité de l'email
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400
        #---------------------------------------------------------------------
        """Register a new user"""

        # Vérification manuelle du mot de passe (vide)
        password = user_data.get('password', '').strip()
        if not password:
            return {'error': 'Password cannot be empty'}, 400

        try:
            new_user_admin = facade.create_user(user_data)
        except ValueError as error :
            return {'error': str(error)}, 400
        # Retourne les info du nouvel utilisateur avec un code 201 ("created")
        return {
            'id': new_user_admin.id,
            'first_name': new_user_admin.first_name,
            'last_name': new_user_admin.last_name,
            'email': new_user_admin.email,
            'is_admin': new_user_admin.is_admin,
            }, 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid data or email already in use')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @api.doc(description="Update an existing user (admin only)")
    def put(self, user_id):
        """
        Update details of an existing user.
        """
#--------------------------Code donnée de user--------------------------------#

        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        # Ensure email uniqueness
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

#-------------------------Notre code de user----------------------------------#

        # Logic to update user details
        if not data:
            return {"error": "Data not found"}, 400

        #if str(current_user["id"]) != str(user_id):
            #return {'error': "Unauthorized action"}, 403

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            user = facade.update_user(user_id, data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

#-----------------------------------------------------------------------------#
#---------------------------------Amenities-----------------------------------#
#-----------------------------------------------------------------------------#

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity created successfully')
    @api.response(400, 'Amenity already registered')
    @api.response(403, 'Admin privileges required')
    @api.doc(description="Create a new amenity (admin only)")
    def post(self):
        """
        Create a new amenity.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # ----------------------------------------------------------------
        # Logic to create a new amenity
        amenity_data = request.json
        name = amenity_data.get('name')
        existing_amenity = facade.get_amenity(name)
        if existing_amenity:
            return {'error': 'Amenity already registered'}, 400

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Missing or invalid data')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.doc(description="Update an existing amenity (admin only)")
    def put(self, amenity_id):
        """
        Update an existing amenity.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

# -----------------------------------------------------------------
# Logic to update an amenity
        amenity_data = request.json
        if not amenity_data:
            return {"error": "Missing data"}, 400
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        # If update was successful, return a confirmation
        if amenity:
            return {"message": "Amenity updated successfully by the admin"}, 200
        else:
            return {"error": "Amenity not found"}, 404


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid or missing data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.doc(description="Update a place as admin or as the owner")
    def put(self, place_id):
        """
        Update details of a place.
        """
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

#----------------------------------------------------------------------------
        # Logic to update the place
        data = request.json
        if not data:
            return {"error": "data not found"}, 400
        # si aucune données n'est envoyé dans postman ou autre

        try:
            # essaie de mettre à jour le lieu
            place = facade.update_place(place_id, data)
        except ValueError as error:
            message = str(error)
            # si le message retour contient not found, retourne 404 .lower évite les erreurs de case
            if "not found" in message.lower():
                return {'error': message}, 404
            # pour les autres erreurs renvoie 400
            return {'error': message}, 400
        # Si mise à jour ok
        return {"message": "Place updated successfully"}, 200
