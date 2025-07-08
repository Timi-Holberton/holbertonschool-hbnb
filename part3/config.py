"""
Configuration module for the Flask application.

Defines base configuration class 'Config' with common settings, including:
- SECRET_KEY fetched from environment variable or defaulted.
- DEBUG flag set to False for production.

Defines 'DevelopmentConfig' class that inherits from 'Config' and overrides/adds:
- DEBUG mode enabled for detailed error output during development.
- SQLite database URI for local development.
- SQLAlchemy tracking disabled to save resources.
- JWT access token expiration set to 1 day.

Also provides a 'config' dictionary to select the configuration class based on the environment.
"""
import os
from datetime import timedelta

class Config:
    """ Class that allows you to store the key """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
# avec la variable d'environnement SECRET_KEY.
# On la stock dans une variable d'environnement car sinon la clé deviens public
# Cela rend l'application plus portable, sécurisée, et facile à configurer
# dans différents environnements (développement, test, production...).
# Ce code signifie donc, essaie d'obtenir la variable d'environnement SECRET_KEY,
# si elle existe pas, utilise 'default_secret_key' comme valeur par défaut
    DEBUG = False
# signifie mode production
# En cas d’erreur, Flask cache les détails techniques.
# Il affiche juste un message générique : "Une erreur est survenue" (ou une page 500).
# Cela protège tes données sensibles, ton code source et empêche les pirates de comprendre la structure de ton app.
# alors que le debug True est plus utilisé dans un cadre de développement sans de grosse sécurité


class DevelopmentConfig(Config):

    """
    Configuration class specific to development.

    Inherits from the main Config class and adds some additional settings:
    - Enable DEBUG mode to display detailed errors.
    - Use a local SQLite database.
    - Disable SQLAlchemy change tracking to save memory.
    - Set a JWT token expiration time of one day.
    """
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    # Définit l'URI de la base de données SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    # Désactive le suivi des modifications d'objet SQLAlchemy, une fonctionnalité qui peut consommer de la mémoire supplémentaire.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Expiration du token JWT fixée à 1 jour
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # Dictionnaire permettant de choisir la configuration selon l'environnement
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
