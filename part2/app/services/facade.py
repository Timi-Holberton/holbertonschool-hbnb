#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

# tu importes une classe qui permetde stocker des données en mémoire


class HBnBFacade:

    """ Front end for managing business operations related to the HBnB application."""

    def __init__(self):
        """ Initialises the HBnBFacade object with in-memory repositories for each entity. """
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
        # on retourne un utilisateur par son ID

    def get_all(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]
        # on retourne une liste

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
        # Permet de chercher un utilisateurà partir de son email

    def update_user(self, user_id, data):
        # Appelle la méthode 'update' du repository pour modifier l'utilisateur existant
        # Cette méthode modifie directement l'objet en mémoire, mais ne retourne rien
        self.user_repo.update(user_id, data)

        # Une fois les données mises à jour, on récupère l'objet utilisateur actualisé
        # Cela permet de s'assurer qu'on renvoie bien les nouvelles données à l'API
        user = self.user_repo.get(user_id)

        # Retourne l'utilisateur mis à jour à l'appelant (typiquement, l'API)
        return user

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son identifiant unique"""
        return self.user_repo.get_by_attribute('id', user_id)

#---------------------------------------------------------------------------#
#------------------------------Anenities------------------------------------#
#---------------------------------------------------------------------------#

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        amenity = self.amenity_repo.get(amenity_id)
        return amenity

#---------------------------------------------------------------------------#
#--------------------------------Place--------------------------------------#
#---------------------------------------------------------------------------#


# pensez à mettre des exceptions  !!!!!!!!!!!
# Implémentez ces validations à l’aide de setters de propriétés dans la Placeclasse pour price, latitude, longitude

    def create_place(self, place_data):
        # Extraire l'identifiant du propriétaire à partir des données reçues
        owner_id = place_data.get("owner_id")
        if not owner_id:
            # Vérifie que l'identifiant du propriétaire est bien fourni
            raise ValueError("owner_id est requis")

        # Vérifie que l'utilisateur correspondant à l'identifiant existe
        user = self.get_user_by_id(owner_id)
        if not user:
            raise ValueError("Aucun utilisateur trouvé avec cet ID")

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

        # Retourne l'objet place nouvellement créé
        return place

    def get_place(self, place_id):
        """ fonction qui ajoute un nouveau lieu"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """ fonction qui ajoute plusieurs lieux """
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        # Récupérer le lieu à mettre à jour à partir de son identifiant
        place = self.get_place(place_id)
        if not place:
            # Si le lieu n'existe pas, lever une exception
            raise ValueError("Place introuvable")

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

        # Retourner l'objet place mis à jour
        return place

#---------------------------------------------------------------------------#
#-------------------------------review--------------------------------------#
#---------------------------------------------------------------------------#

    def create_review(self, review_data):
        # Espace réservé pour la logique de création d'un avis, incluant la validation
        # de user_id, place_id et rating
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        # Espace réservé pour la logique de récupération d’un avis par son ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Espace réservé pour la logique de récupération de tous les avis
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        # Espace réservé pour la logique de récupération de tous les avis pour un lieu spécifique
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        # Espace réservé pour la logique de mise à jour d’un avis
        self.review_repo.update(review_id, review_data)
        review = self.review_repo.get(review_id)
        return review

    def delete_review(self, review_id):
        # Espace réservé pour la logique de suppression d’un avis
        return self.review_repo.delete(review_id)
