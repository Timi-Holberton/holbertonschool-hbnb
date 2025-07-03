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
    'is_admin': fields.Boolean(required=False, description='Administrator status'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()    
    @api.expect(user_model, validate=True)  # Active la validation automatique,
    @api.response(201, 'User_admin successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Invalid input data')
    def post(self):
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
        
        # Hachage du mot de passe
        user_data['password'] = generate_password_hash(user_data['password'])

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
    def put(self, user_id):
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
            'is-admin': user.is_admin
        }, 200

#-----------------------------------------------------------------------------#
#---------------------------------Amenities-----------------------------------#
#-----------------------------------------------------------------------------#

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
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
    def put(self, amenity_id):
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
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
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
