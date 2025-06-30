import os


class Config:
    """ Class that allows you to store the key """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
# avec la variable d'environnement SECRET_KEY.
# On la stock dans une variable d'environnement car sinon la clé deviens public
# Cela rend l'application plus portable, sécurisée, et facile à configurer
# dans différents environnements (développement, test, production...).
# Ce code signifie donc, essaie d'obtenir la variable d'environnement SECRET_KEY,
# si elle existe pas, utilise 'default_secret_key' comme valeut par défaut
    DEBUG = False
# signifie mode production
# En cas d’erreur, Flask cache les détails techniques.
# Il affiche juste un message générique : "Une erreur est survenue" (ou une page 500).
# Cela protège tes données sensibles, ton code source et empêche les pirates de comprendre la structure de ton app.
# alors que le debug True est plus utilisé dans un cadre de développement sans de grosse sécurité
    

class DevelopmentConfig(Config):

    """ 
    Configuration class specific to development.

    - DEBUG enabled: displays detailed errors to facilitate testing.
    - Inherits from Config, so also retrieves the SECRET_KEY.
    """

    DEBUG = True
    # True servira juste pour la partie développement pour les tests du développeur

    # Dictionnaire permettant de choisir la configuration selon l'environnement
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
