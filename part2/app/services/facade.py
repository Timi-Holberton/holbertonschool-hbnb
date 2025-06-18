#!/usr/bin/env python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User

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

    # Placeholder method for fetching a place by ID

    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        # Puis récupère l'objet mis à jour avec get()
        user = self.user_repo.get(user_id)
        return user
