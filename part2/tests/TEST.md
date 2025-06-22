# Tests Unitaires de l'API HBnB

Pour garantir le bon fonctionnement de l’API HBnB, nous avons mis en place des tests unitaires complets en combinant deux approches complémentaires :

- **Tests fonctionnels automatisés avec Postman**  
  Ces tests simulent des requêtes HTTP sur tous les endpoints de l’API, vérifiant les statuts de réponse, les données retournées et la gestion des erreurs.
  Ils permettent de valider le comportement global de l’API en conditions réelles.

- **Tests unitaires en Python avec unittest**  
  Ces tests ciblent la logique interne du backend, en vérifiant le fonctionnement des fonctions, la validation des données et la gestion des exceptions.
  Ils garantissent la robustesse du code et facilitent la détection rapide des régressions.

Cette double approche assure à la fois la conformité fonctionnelle pour les utilisateurs et la qualité du code pour les développeurs.

📄 [Documentation test (PDF)](TEST_Units_Places_and_Reviews.pdf)
