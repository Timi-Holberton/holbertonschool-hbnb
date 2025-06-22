from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

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

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        title = place_data.get('title')
        existing_place = facade.get_place(title)
        if existing_place:
            return {'error': 'the place already exists'}, 409
        owner_id = place_data.get('owner_id')
        user = facade.get_user_by_id(owner_id)
        if not user:
            return {'error': "propriétaire non trouvé"}, 400
        new_place = facade.create_place(place_data)
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
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'The place does not exist'}, 404

        # Récupérer le User (owner)
        owner = facade.get_user_by_id(place.owner_id)
        if owner:
            owner_data = owner.to_dict()
        else:
            owner_data = None


        # Récupérer les amenities (déjà des objets), récupère le dictionnaire
        # dans la classe place
        amenities_data = [a.to_dict() for a in place.amenities]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenities_data
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        data = request.json
        # le serveur reçoit la requêteet le coprs de la requête contient des
        # données au format JSON
        # parsing automatique du corps de la requête pour obtenir un dictionnaire Python (ou objet) correspondant au JSON envoyé.
        if not data:
            return {"error": "Données manquantes"}, 400

        place = facade.update_place(place_id, data)

        if place:
            return {
                'title': place.title,
                'description': place.description,
                'price': place.price
            }, 200
        else:
            return {"error": "Le lieu n'existe pas"}, 404

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
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
