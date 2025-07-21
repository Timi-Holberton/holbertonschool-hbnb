"""
Place management module (places) via a RESTful API using Flask-RESTx.

This module defines a namespace dedicated to managing places,
providing endpoints for creating, retrieving, updating places,
and accessing reviews associated with each place.

Main functionalities:
- POST /places/                  : Create a new place (authentication required).
- GET /places/                   : Retrieve the list of all places.
- GET /places/<place_id>         : Retrieve details of a place by its ID.
- PUT /places/<place_id>         : Update an existing place (only allowed by the owner, authentication required).
- GET /places/<place_id>/reviews : Retrieve all reviews linked to a place.

Data validation and API documentation are managed via Flask-RESTx models.

Business logic and data access are delegated to the 'facade' service.

Security:
- JWT authentication is required to create or update places.
- Only the owner of a place can update its details.

HTTP status codes used:
- 200 : Operation successful.
- 201 : Resource successfully created.
- 400 : Invalid or missing data.
- 403 : Unauthorized action.
- 404 : Resource not found.
- 409 : Conflict (e.g., place title already exists).
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Create a namespace for place-related endpoints
api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'The place already exists')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        # Check if a place with the same title already exists

        current_user = get_jwt_identity()
        place_data['owner_id'] = current_user['id']

        title = place_data.get('title')
        existing_place = facade.get_place(title)

        if existing_place:
            return {'error': 'the place already exists'}, 409
            
        user = facade.get_user_by_id(current_user['id'])
        if not user:
            return {'error': "owner not found"}, 400

        try:
            new_place = facade.create_place(place_data)
        # str(e) contient le texte du message d’erreur qui a été donné 
        # lors du raise de l’exception dans la classe model
        except ValueError as error:
            return {'error': str(error)}, 400

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        place = facade.get_all_places()
        if place:
            return place, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', model=place_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a specific place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'The place does not exist'}, 404

        # Récupérer le User (owner)
        owner = facade.get_user_by_id(place.owner_id)
        if owner:
            owner_data = owner.to_dict()
        else:
            owner_data = None


        # Fetch amenities related to the place
        amenities_data = [a.to_dict() for a in place.amenities]
        reviews_data = [a.to_dict() for a in place.reviews]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenities_data,
            'reviews': reviews_data
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def put(self, place_id):
        """Update the details of a specific place"""
        # Récupérer les données JSON envoyées dans la requête
        data = request.json
        if not data:
            return {"error": "data not found"}, 400
        # si aucune données n'est envoyé dans postman ou autre

        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if str(place.owner_id) != str(current_user['id']):
            return {'error': 'Unauthorized action'}, 403


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


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully', model=[review_model])
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        # vérifie si le lieu existe bien
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        # ensuite on récupère tous les avis du lieu
        reviews = facade.get_reviews_by_place(place_id)
        # On retourne la liste formatée (même si elle est vide)
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            }
            for review in reviews
        ], 200
