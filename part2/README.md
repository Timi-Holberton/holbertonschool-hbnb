Welcome to the HBNB - BL and API project

## Presentation

HBnB is a RESTful API inspired by the AirBnB website, developed in Python with Flask and Flask-RESTX. The project follows a three-layer architecture developed in part 1 of the HBnB project.

To run the application, you will need:

1) Install dependencies using: 
    - pip install -r requirements.txt
2) Run the application: 
    - python run.py

the application should be running

## Purpose of each directory and file:

├── app/ : is the directory that contains the main application code.
│   ├── __init__.py : constructor of app
│   ├── api/ : subdirectory of app that hosts the API endpoints, organised by version ( v1/).
│   │   ├── __init__.py : constructeur of the API
│   │   ├── v1/ : First version of the API, which will contain useful information
│   │       ├── __init__.py : constructor of the first version of API
│   │       ├── users.py : User Route
│   │       ├── places.py : Place Route
│   │       ├── reviews.py : Reviews Route
│   │       ├── amenities.py : Amenities Route 
│   ├── models/ : subdirectory contains the business logic classes
│   │   ├── __init__.py : constructor of the models
│   │   ├── user.py : User models
│   │   ├── place.py : Place models
│   │   ├── review.py : Review models
│   │   ├── amenity.py : Amenity models
│   ├── services/ : subdirectory. The Facade model will be implemented, managing the interaction between the layers.
│   │   ├── __init__.py : constructor of the facade
│   │   ├── facade.py : enables interaction between the different layers
│   ├── persistence/ : subdirectory. This is where the in-memory repository is implemented. It will eventually be replaced by a database-based solution using SQL Alchemy.
│       ├── __init__.py
│       ├── repository.py
├── run.py : is the entry point for running the Flask application.
├── config.py : will be used to configure environment variables and application settings.
├── requirements.txt : lists all Python packages required for the project.
├── README.md : contains a brief overview of the project.

