"""
Amenity management module via a RESTful API.

This module defines a Flask-RESTx namespace for managing amenities,
providing endpoints to create, retrieve, update, and list amenities.

Available endpoints:
- POST /amenities/       : Create a new amenity.
- GET /amenities/        : Retrieve the list of all amenities.
- GET /amenities/<id>    : Retrieve a specific amenity by its ID.
- PUT /amenities/<id>    : Update an existing amenity.

Each endpoint uses input validation through Flask-RESTx models
and returns appropriate HTTP status codes based on operation results.

The module relies on the 'facade' service for data access and business logic.

Handled exceptions and responses:
- 201 : Resource successfully created.
- 200 : Successful retrieval or update.
- 400 : Invalid input data or amenity already exists.
- 404 : Amenity not found.
"""


from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create a namespace for all amenity-related endpoints
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or amenity already exists')
    def post(self):
        """Register a new amenity"""
        # Retrieve the JSON payload from the request
        amenity_data = api.payload
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

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all available amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = request.json
        if not amenity_data:
            return {"error": "Missing data"}, 400
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as error:
            return {'error': str(error)}, 400

        # If update was successful, return a confirmation
        if amenity:
            return {"message": "Amenity updated successfully"}, 200
        else:
            return {"error": "Amenity not found"}, 404
