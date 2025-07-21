#!/usr/bin/env python3

"""
Facade class for managing business logic related to the HBnB application.

This class acts as a front-end interface to handle operations on core entities:
users, places, reviews, and amenities. It abstracts the underlying data
repositories and provides methods for creating, retrieving, updating, and deleting
these entities, enforcing necessary validations and relationships.

Main features:
- Manage User entities: creation, retrieval (by ID or email), update.
- Manage Amenity entities: creation, retrieval, update.
- Manage Place entities: creation (with owner and amenities association), retrieval,
  update (including amenities update).
- Manage Review entities: creation (linked to user and place), retrieval, update,
  deletion.
- Validation of entity existence and integrity before operations.
- Handles relationships between entities (e.g., associating amenities with places,
  linking reviews to users and places).

Exceptions:
- Raises ValueError for invalid or missing data.
- Handles cases where referenced entities (e.g., users, places) do not exist.

Note:
- Uses in-memory repositories to store entity instances.
- The facade abstracts persistence details from higher-level API layers.
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError # pour interdire doublon place
from app import db

class HBnBFacade:

    """ Front end for managing business operations related to the HBnB application."""

    def __init__(self):
        """ Initialises the HBnBFacade object with in-memory repositories for each entity. """
        self.user_repo = UserRepository()  # Switched to SQLAlchemyRepository
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """ Creates a new user based on the data provided """
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        db.session.commit()
        return user

    def get_user(self, user_id):
        """ Retrieves a user by their unique ID """
        return self.user_repo.get(user_id)
        # on retourne un utilisateur par son ID

    def get_all(self):
        """ Returns a list of all users in the form of dictionaries."""
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]
        # on retourne une liste

    def get_user_by_email(self, email):
        """ Search for a user based on their email address """
        return self.user_repo.get_by_attribute('email', email)
        # Permet de chercher un utilisateurà partir de son email

    def update_user(self, user_id, data):
        """ Updates the data of an existing user """
        # Appelle la méthode 'update' du repository pour modifier l'utilisateur existant
        # Cette méthode modifie directement l'objet en mémoire, mais ne retourne rien
        self.user_repo.update(user_id, data)

        # Une fois les données mises à jour, on récupère l'objet utilisateur actualisé
        # Cela permet de s'assurer qu'on renvoie bien les nouvelles données à l'API
        user = self.user_repo.get(user_id)
        db.session.commit()
        # Retourne l'utilisateur mis à jour à l'appelant (typiquement, l'API)
        return user

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son identifiant unique"""
        return self.user_repo.get_by_attribute('id', user_id)

#---------------------------------------------------------------------------#
#------------------------------Anenities------------------------------------#
#---------------------------------------------------------------------------#

    def create_amenity(self, amenity_data):
        """ Creates a new amenity based on the data provided """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity(self, amenity_id):
        """ return a specific amenities with ID """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """ return all of amenities """
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        """ update a amenity """
        # Récupère l'amenity en mémoire à partir de son ID
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            # Pas trouvé donc on retourne None = ID inconnu
            return None
        try:
            # essaie de mettre à jour, doit valider les données et lever ValueError
            amenity.update(amenity_data)
        except ValueError as error:
            # Relance l'exception pour que l'API la gère
            raise error
        # si ok, retourne amenity modifié
        db.session.commit()
        return amenity

#---------------------------------------------------------------------------#
#--------------------------------Place--------------------------------------#
#---------------------------------------------------------------------------#

    def create_place(self, place_data):
        """ Creates a new amenity based on the data provided """
        # Extraire l'identifiant du propriétaire à partir des données reçues
        owner_id = place_data.get("owner_id")
        if not owner_id:
            # Vérifie que l'identifiant du propriétaire est bien fourni
            raise ValueError("owner_id est requis")

        # Vérifie que l'utilisateur correspondant à l'identifiant existe
        user = self.get_user_by_id(owner_id)
        if not user:
            raise ValueError("Aucun utilisateur trouvé avec cet ID")

        # Vérification avant création pour éviter doublon
        existing_place = Place.query.filter_by(title=place_data['title'], owner_id=owner_id).first()
        if existing_place:
            raise ValueError("This Place already exist for this owner.")

        # Extraire la liste des identifiants des commodités (amenities) depuis les données
        # On les retire du dictionnaire pour éviter de les passer au constructeur de Place
        amenity_ids = place_data.pop("amenities", [])

        # Créer une nouvelle instance de Place avec les données restantes
        place = Place(**place_data)

        # Associer les objets Amenity à l'objet Place
        for amenity_id in amenity_ids:
            # Récupère l'objet Amenity correspondant à l'identifiant
            amenity = self.get_amenity(amenity_id)
            if amenity:
                # Ajoute l'amenity à la liste des commodités de la place
                place.add_amenity(amenity)

        # Enregistre la nouvelle place dans le dépôt (base de données ou autre persistance)
        self.place_repo.add(place)
##---------------------------------------------------------------------------##
##---------------------------------------------------------------------------##
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Place already exist with this title for this owner")

# Tente de valider les modifications dans la base de données avec commit().
# Si une contrainte d'intégrité est violée (par exemple un doublon unique),
# une exception IntegrityError est levée.
# On effectue alors un rollback() pour annuler la transaction en cours,
# ce qui permet de garder la session SQLAlchemy propre et prête à d'autres opérations.
# Enfin, on lève une ValueError avec un message clair pour informer l'utilisateur
# que la donnée existe déjà et éviter un message d'erreur technique brut.

##---------------------------------------------------------------------------##
##---------------------------------------------------------------------------##

        db.session.commit()
        # Retourne l'objet place nouvellement créé
        return place

    def get_place(self, place_id):
        """ function that displays a specific location"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """ function that displays multiple locations """
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        """ Update a place """
        # Récupérer le lieu à mettre à jour à partir de son identifiant
        place = self.get_place(place_id)
        if not place:
            # Si le lieu n'existe pas, lever une exception
            raise ValueError("Place not found")

        # Extraire la liste des identifiants d'amenities si elle est fournie
        # On la retire du dictionnaire pour éviter de l'envoyer à update()
        amenities_ids = place_data.pop("amenities", None)

        # Mettre à jour les attributs de l'objet place avec les nouvelles données
        place.update(place_data)

        if amenities_ids is not None:
            # Si une nouvelle liste d'amenities est fournie,
            # on réinitialise la liste actuelle
            place.amenities = []
            for amenity_id in amenities_ids:
                # Récupérer chaque objet Amenity correspondant à l'identifiant
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    # Ajouter l'amenity à la liste de la place
                    place.add_amenity(amenity)

        db.session.commit()

        # Retourner l'objet place mis à jour
        return place

    def get_place_by_id(self, place_id):
        """ Retrieves a user by their unique ID """
        return self.place_repo.get_by_attribute('id', place_id)

#---------------------------------------------------------------------------#
#-------------------------------review--------------------------------------#
#---------------------------------------------------------------------------#

    def create_review(self, review_data):
        """ Creates a new review based on the data provided (user et place) """
        # Récupérer les IDs dans les données reçues
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        # Validation des IDs
        if not user_id:
            raise ValueError("user_id est requis")
        if not place_id:
            raise ValueError("place_id est requis")

        # Récupérer les objets User et Place associés
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Aucun utilisateur trouvé avec l'ID {user_id}")

        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Aucun lieu trouvé avec l'ID {place_id}")

        # Extraire les autres champs nécessaires à Review
        text = review_data.get('text')
        rating = review_data.get('rating')

        # Création d'une instance Review avec le texte, la note,
        # l'identifiant utilisateur (UUID) et l'identifiant lieu (UUID) récupérés depuis les objets user et place
        review = Review(text=text, rating=rating, user_id=user.id, place_id=place.id)

        # Ajouter la review dans le dépôt (base de données ou autre persistance)
        self.review_repo.add(review)
        db.session.commit()
        # Retourner l’objet Review créé
        return review

    def get_review(self, review_id):
        """ list a specific review"""
        # Espace réservé pour la logique de récupération d’un avis par son ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """ resume the lists of all reviews """
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        """ obtain a review by the place who choosen"""
        # Espace réservé pour la logique de récupération de tous les avis pour un lieu spécifique
        all_reviews = self.review_repo.get_all()
        filtered_reviews = []

        for review in all_reviews:
            if review.place and review.place.id == place_id:
                filtered_reviews.append(review)

        return filtered_reviews

    def update_review(self, review_id, review_data):
        """ update a review """
        # Espace réservé pour la logique de mise à jour d’un avis
        self.review_repo.update(review_id, review_data)
        review = self.review_repo.get(review_id)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        """ delete a review """
        # Espace réservé pour la logique de suppression d’un avis
        # Vérifie d'abord si la review existe
        review = self.review_repo.get(review_id)
        if not review:
            return False  # Ne rien supprimer si l'ID est inconnu

        # Supprime la review
        self.review_repo.delete(review_id)
        db.session.commit()
        # Confirme qu'elle n'existe plus
        return True


