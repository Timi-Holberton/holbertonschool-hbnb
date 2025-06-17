Bienvenue dans le projet HBNB - BL and API

## Présentation

HBnB est une API RESTful inspirée du site AirBnB, développée en Python avec Flask et Flask-RESTX. Le projet suit une architecture en trois couches développée dans la partie 1 du projet HBnB.

pour éxécuter l'application il faudra : 

1) Installer les dépendances en utilisant : 
	- pip install -r requirements.txt
2) Exécuter l'application : 
	- python run.py

l'application devrait être en cours d'exécution 

## But de chaque répertoire et fichier :

├── app/ : est le répertoire qui contient le code principal de l'application.
│   ├── __init__.py : constructeur qui contient toutes les informations des répertoires de app
│   ├── api/ : sous-répertoire de app qui héberge les points de terminaison de l'API, organisés par version ( v1/).
│   │   ├── __init__.py : constructeur qui contient toutes les informations de l'API
│   │   ├── v1/ : 1ère version de l'API qui va contenir des informations utiles
│   │       ├── __init__.py : constructeur qui contient les informations de chaques users, place, review et amenities
│   │       ├── users.py : Route utilisateur
│   │       ├── places.py : Route place
│   │       ├── reviews.py : Route reviews
│   │       ├── amenities.py : Route amenities
│   ├── models/ : sous-répertoire contient les classes de logique métier
│   │   ├── __init__.py : constructeur qui contiendra tout ce qu'il faut pour la logique métier
│   │   ├── user.py : Class User
│   │   ├── place.py : Class place
│   │   ├── review.py : Class review
│   │   ├── amenity.py : Class amenity
│   ├── services/ : sous-répertoire est l'endroit où le modèle Facade est implémenté, gérant l'interaction entre les couches.
│   │   ├── __init__.py : constructeur qui contient les méthodes de la façade
│   │   ├── facade.py : fichier façade qui permet l'interaction entre les différentes couches
│   ├── persistence/ : sous-répertoire est l'emplacement où le référentiel en mémoire est implémenté. Il sera ultérieurement remplacé par une solution basée sur une base de données utilisant SQL Alchemy.
│       ├── __init__.py
│       ├── repository.py
├── run.py : est le point d'entrée pour l'exécution de l'application Flask.
├── config.py : sera utilisé pour configurer les variables d'environnement et les paramètres de l'application.
├── requirements.txt : liste tous les packages Python nécessaires au projet.
├── README.md : contiend un bref aperçu du projet.

# Copyright (c) 2025 [Robin et Timi - Holberton School]
# All rights reserved.

# This file is part of HBnB project and is licensed under the MIT License.

