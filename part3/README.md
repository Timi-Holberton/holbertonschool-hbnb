# Welcome to the HBNB - BL and API Project

## Presentation

HBnB is a RESTful API inspired by the AirBnB website, developed in Python with Flask and Flask-RESTX.  
The project follows a three-layer architecture developed in part 1 of the HBnB project.

### To run the application

1. Install dependencies using:
   `pip install -r requirements.txt`
2. Run the application:
   `python3 run.py`
3. If you want to run the test:
   `python3 run_tests.py`

The application should now be running.

---

## Purpose of each directory and file

![Structure du projet](structure.png)

# >>> from app import create_app, db
# >>> app = create_app()
# >>> app.app_context().push()  # <-- Active le contexte Flask
# >>> db.create_all()  # <-- Fonctionne maintenant !
pour la créaton d'une base de donnée

## Commande pour le lancement du script SQL

sqlite3 instance/development.db < app/database/schema.sql

### Diagramme de base de données

```mermaid
erDiagram
    USERS {
        %% PK Primary Key
        CHAR(36) id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }
    PLACES {
        CHAR(36) id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        %% Foreign Key
        CHAR(36) owner_id FK
    }
    REVIEWS {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }
    AMENITIES {
        CHAR(36) id PK
        VARCHAR name
    }
    PLACE_AMENITY {
        CHAR(36) place_id FK
        CHAR(36) amenity_id FK
    }
    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES ||--o{ PLACE_AMENITY : has
    %% Table d'association pour relation many-to-many entre Place et Amenity
    AMENITIES ||--o{ PLACE_AMENITY : linked_to
```
