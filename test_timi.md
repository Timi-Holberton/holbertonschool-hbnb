@startuml
!theme cerulean-outline
title Architecture 3 couches du projet HBnB

package "Presentation Layer" {
    [API Services] as apiGateway
    [UserAPI]
    [PlaceAPI]
    [ReviewAPI]
    [AmenityAPI]
}

note top of apiGateway
L’API principale reçoit toutes les requêtes externes (Utilisateurs ou clients).
Elle applique d’abord les fonctionnalités transversales (authentification, logging, limitation de requêtes, etc.).
Ensuite, elle dirige chaque requête vers la sous-API spécialisée qui gère le domaine concerné.
end note

note top of UserAPI
Les sous-API sont des modules spécialisés,
  chacun dédié à un domaine précis
Elles reçoivent les requêtes de l’API principale,
  gèrent les opérations spécifiques à leur domaine,
  puis transmettent les demandes à la logique métier via la façade.
Cette organisation modulaire simplifie le code, facilite la maintenance,
  et permet d’appliquer des règles propres à chaque domaine
  tout en évitant que l’API principale devienne trop complexe.
end note

package "Business Logic Layer" {
    [Facade] as facade

    [User Model] as userModel
    [Place Model] as placeModel
    [Review Model] as reviewModel
    [Amenity Model] as amenityModel
}

note top of facade
La façade oriente les appels vers la bonne logique métier,
  simplifiant les interactions.
Elle organise et facilite le travail avec les données.
Elle fait le lien entre la présentation et les données.
end note

note top of userModel
Ces "modèles" représentent les objets importants :
Utilisateur, Lieu, Avis, Équipement.
Ils contiennent les règles du métier par exemple :
→ Le prix total dépend du nombre de nuits.
→ Un utilisateur ne peut pas réserver un lieu dans le passé.
→ Un avis ne peut être posté que si une réservation existe.
end note

package "Persistence Layer" {
    [UserRepository] as userRepo
    [PlaceRepository] as placeRepo
    [ReviewRepository] as reviewRepo
    [AmenityRepository] as amenityRepo
    [Base de données] as database
}

note top of userRepo
Un Repository (dépôt) est une interface entre la logique métier
  et la base de données.
Il permet à la couche métier de "parler" à la base de données
  sans s’occuper des détails techniques.
Il centralise l’accès aux données
(lecture, écriture, mise à jour, suppression).
Il cache les détails techniques
(comme les requêtes SQL ou les appels ORM).
Il sépare les responsabilités :
→ La logique métier se concentre sur le métier,
→ Le repository se concentre sur la persistance des données.
end note

note top of database
Une base de données contient des tables
qui ressemblent à des tableaux Excel.
Chaque table est composée de colonnes
(attributs) et de lignes (enregistrements).
Chaque ligne possède une clé primaire
qui l'identifie de manière univoque cet enregistrement.
Pour interagir avec la base de données,
on utilise des requêtes SQL (bas lvl).
Pour faciliter le travail, les développeurs
utilisent souvent un ORM (Object-Relational Mapping),
qui traduit les opérations en SQL en manipulations
d’objets dans le langage de programmation (haut lvl).
end note

' Connexions entre les composants

apiGateway --> UserAPI : Transmet à
apiGateway --> PlaceAPI : Transmet à
apiGateway --> ReviewAPI : Transmet à
apiGateway --> AmenityAPI : Transmet à

UserAPI --> facade : Demande à
PlaceAPI --> facade : Demande à
ReviewAPI --> facade : Demande à
AmenityAPI --> facade : Demande à

facade --> userModel : Utilise
facade --> placeModel : Utilise
facade --> reviewModel : Utilise
facade --> amenityModel : Utilise

userModel --> userRepo : Accède à
placeModel --> placeRepo : Accède à
reviewModel --> reviewRepo : Accède à
amenityModel --> amenityRepo : Accède à

userRepo --> database : Requête SQL
placeRepo --> database : Requête SQL
reviewRepo --> database : Requête SQL
amenityRepo --> database : Requête SQL

@enduml
