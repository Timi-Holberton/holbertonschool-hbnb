#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

# tu importes une classe qui permetde stocker des données en mémoire


class HBnBFacade:
    def __init__(self):
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


# CHEZ TIMI !!


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
        self.user_repo.update(amenity_id, amenity_data)
        amenity = self.user_repo.get(amenity_id)
        return amenity


# CHEZ ROBIN
# pensez à mettre des exceptions et ajouter les importation !!!!!!!!!!!
# Implémentez ces validations à l’aide de setters de propriétés dans la Placeclasse pour price, latitude, longitude


    def create_place(self, place_data):
        """ fonction qui créé un nouveau lieu """
        place = Place(**place_data)
        self.user_repo.add(place)
        return place

    def get_place(self, place_id):
        """ fonction qui ajoute un nouveau lieu"""
        return self.user_repo.get(place_id)

    def get_all_places(self):
        """ fonction qui ajoute plusieurs lieux """
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    def update_place(self, place_id, place_data):
        """ fonction qui met à jour un lieu"""
        self.place_repo.update(place_id, place_data)
        place = self.place_repo.get(place_id)
        return place
