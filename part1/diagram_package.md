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

package "Business Logic Layer" {
    [Facade] as facade
    [Base Model] as baseModel
    [User Model] as userModel
    [Place Model] as placeModel
    [Review Model] as reviewModel
    [Amenity Model] as amenityModel
}

package "Persistence Layer" {
    [UserRepository] as userRepo
    [PlaceRepository] as placeRepo
    [ReviewRepository] as reviewRepo
    [AmenityRepository] as amenityRepo
    [Base de données] as database
}

' Connexions entre les composants
apiGateway --> UserAPI : Transmet à
apiGateway --> PlaceAPI : Transmet à
apiGateway --> ReviewAPI : Transmet à
apiGateway --> AmenityAPI : Transmet à

UserAPI --> facade : Délègue à
PlaceAPI --> facade : Délègue à
ReviewAPI --> facade : Délègue à
AmenityAPI --> facade : Délègue à

userModel -[#green]|> baseModel : hérite
placeModel -[#green]|> baseModel : hérite
reviewModel -[#green]|> baseModel : hérite
amenityModel -[#green]|> baseModel : hérite


facade --> userModel : Utilise
facade --> placeModel : Utilise
facade --> reviewModel : Utilise
facade --> amenityModel : Utilise

userModel --> userRepo : Accède à
placeModel --> placeRepo : Accède à
reviewModel --> reviewRepo : Accède à
amenityModel --> amenityRepo : Accède à
 
userRepo --> database : Requêtes SQL
placeRepo --> database : Requêtes SQL
reviewRepo --> database : Requêtes SQL
amenityRepo --> database : Requêtes SQL
@enduml
