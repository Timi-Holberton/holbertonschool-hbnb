from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Récupérer l'email et le mot de passe depuis les données de la requête


        # Étape 1 : Récupérer l'utilisateur à partir de l'email fourni et on 
        user = facade.get_user_by_email(credentials['email'])
        print(f"user found: {user}")
        print(f"user.password: {user.password}")
        print(f"password provided: {credentials['password']}")
        if user:
            print(f"password verify: {user.verify_password(credentials['password'])}")

        # Étape 2 : Vérifier que l'utilisateur existe et que le mot de passe est correct
        
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'User not found or password missing'}, 401

        # Étape 3 : Créer un jeton JWT contenant l'identifiant de l'utilisateur et son statut administrateur
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})


        # Étape 4 : Renvoyer le jeton JWT au client
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur à partir du jeton
        return {'message': f'Hello, user {current_user["id"]}'}, 200

