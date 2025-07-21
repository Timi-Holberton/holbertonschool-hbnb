"""
Singleton instance of the HBnBFacade class.

This 'facade' instance is created to ensure that only one
instance of the HBnBFacade class is used throughout the application,
providing a centralized interface to the application's business logic.
"""

from app.services.facade import HBnBFacade

facade = HBnBFacade()

# Cette facadeinstance sera utilisée comme singleton pour garantir qu'une 
# seule instance de la HBnBFacadeclasse est créée et utilisée 
# dans toute l'application.
