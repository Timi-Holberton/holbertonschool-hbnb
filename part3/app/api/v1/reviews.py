"""
Review management module (reviews) via a RESTful API.

This module defines a Flask-RESTx namespace dedicated to review operations,
with endpoints that allow the creation, retrieval, update, and deletion
of reviews associated with places and users.

Main functionalities:
- POST /reviews/               : Create a new review.
- GET /reviews/                : Retrieve the list of all reviews.
- GET /reviews/<review_id>     : Retrieve a review by its ID.
- PUT /reviews/<review_id>     : Update an existing review.
- DELETE /reviews/<review_id>  : Delete a review by its ID.

Each endpoint uses Flask-RESTx models for input validation
and automatic API documentation (Swagger).

Operations rely on the 'facade' service to handle business logic
and data access.

HTTP status codes used:
- 200 : Operation successful.
- 201 : Resource successfully created.
- 400 : Invalid or missing data.
- 404 : Resource not found.

Error handling includes checking for the existence of associated users and places,
as well as validating the 'rating' field (must be an integer between 1 and 5)
and the 'text' field.
"""


from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a namespace for review-related endpoints
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    # 'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def post(self):
        """Register a new review"""
        # Récupération des données envoyées dans le corps de la requête (format JSON)
        review_data = api.payload

        # Extraction des champs 'user_id' et 'place_id' des données de la review car ils seront utilisés
        user_id = get_jwt_identity()["id"]
        place_id = review_data.get('place_id')

        # présence de l'id du lieu et de l'utilisateur obligatoire
        if not user_id or not place_id:
            return {'error': 'user_id or place_id missing'}, 400

        # on vérifie que le l'utilisateur existe sinon on retourne une erreur
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 400

        # on vérifie que le lieu existe sinon on retourne une erreur
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 400

        print(f"Utilisateur connecté: {user_id}")
        print(f"Propriétaire du lieu: {place.owner.id}")

        # **Vérification que l'utilisateur n'est pas propriétaire du lieu**
        # (adapter l'attribut 'owner' selon ton modèle Place)
        if hasattr(place, 'owner') and str(place.owner.id) == str(user_id):
            return {'error': 'You cannot evaluate your own location.'}, 400

        # Récupère toutes les reviews existantes pour ce lieu
        existing_reviews = facade.get_reviews_by_place(place_id) or []

        # Vérifie si l'utilisateur a déjà posté une review pour ce lieu
        for rev in existing_reviews:
            if rev.user and str(rev.user.id) == str(user_id):
                return {'error': 'You have already reviewed this place'}, 400
        # Si tout est bon, crée une nouvelle review avec les données fournies
        try:
            new_review = facade.create_review(review_data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user.id,
            'place_id': new_review.place.id
        }, 201


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        reviews = facade.get_all_reviews()
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a review by its ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Serialize user and place data if available
        if review.user is not None:
            user_data = review.user.to_dict()
        else:
            user_data = None

        if review.place is not None:
            place_data = review.place.to_dict()
        else:
            place_data = None

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': user_data,
            'place': place_data
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def put(self, review_id):
        """Update a review's information"""
        review_data = request.json
        if not review_data:
            return {"error": "Missing data"}, 400

        # 1. Vérifier si la review existe
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        user_id = get_jwt_identity()["id"]
        if not review.user or str(review.user.id) != str(user_id):
            return {"error": "Unauthorised action"}, 403

        # 2. Valider les données fournies
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return {'error': 'Rating must be an integer between 1 and 5'}, 400

        if 'text' in review_data:
            text = review_data['text'].strip()
            if not text:
                return {'error': 'Review text cannot be empty'}, 400

        # 3. Mettre à jour la review via la façade
        try:
            updated_review = facade.update_review(review_id, review_data)
        except Exception as e:
            # Capture toute erreur inattendue (ex: validation côté modèle)
            return {'error': str(e)}, 400

        # 4. Retourner la review mise à jour
        return {
            'review': {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user': updated_review.user.id if updated_review.user else None,
                'place': updated_review.place.id if updated_review.place else None
            },
            'message': 'Review successfully updated'
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized to delete this review')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, review_id):
        """Delete a review by its ID"""
        # Étape 1 : Récupérer la review
        review_delete = facade.get_review(review_id)
        if not review_delete:
            return {'error': 'Review not found'}, 404

        # Étape 2 : Vérifier que l'utilisateur connecté est bien le propriétaire
        user_id = get_jwt_identity()["id"]
        if not review_delete.user or str(review_delete.user.id) != str(user_id):
            return {"error": " Unauthorised action"}, 403

        # Étape 3 : delete the review
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

