# Journal de Tests API Holberton HBnB

## Structure du journal

| Point final testé      | Méthode HTTP | Données d'entrée                                  | Résultat attendu                          | Résultat réel         | Problèmes rencontrés        |
|------------------------|--------------|---------------------------------------------------|-------------------------------------------|-----------------------|-----------------------------|

---

## Users

### POST /api/v1/users/
- Données d'entrée : 
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/users/
- Données d'entrée : /
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/users/<user_id>
- Données d'entrée : user_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### PUT /api/v1/users/<user_id>
- Données d'entrée : données de mise à jour valides/invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

---

## Amenities

### POST /api/v1/amenities/
- Données d'entrée : 
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/amenities/
- Données d'entrée : /
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/amenities/<amenity_id>
- Données d'entrée : amenity_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### PUT /api/v1/amenities/<amenity_id>
- Données d'entrée : données de mise à jour valides/invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

---

## Places

### POST /api/v1/places/
- Données d'entrée : 
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/places/
- Données d'entrée : /
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/places/<place_id>
- Données d'entrée : place_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### PUT /api/v1/places/<place_id>
- Données d'entrée : données de mise à jour valides/invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/places/<place_id>/reviews
- Données d'entrée : place_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

---

## Reviews

### POST /api/v1/reviews/
- Données d'entrée : 
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/reviews/
- Données d'entrée : /
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### GET /api/v1/reviews/<review_id>
- Données d'entrée : review_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### PUT /api/v1/reviews/<review_id>
- Données d'entrée : données de mise à jour valides/invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

### DELETE /api/v1/reviews/<review_id>
- Données d'entrée : review_id valide ou invalide
- Résultat attendu :
- Résultat réel :
- Problèmes rencontrés :

---

# API Test Log
This section documents the tests performed on the REST API, including:

- Tested endpoints

- Input data

- Expected vs. actual outcomes

- Issues encountered

👤 User Endpoints
POST /users
TC-U1	{ "first_name": "John", "last_name": "Doe", "email": "john@example.com" }	201 Created with user ID	✅ 201 Created	None
TC-U2	Duplicate email	400 Email already registered	✅ 400	None

GET /users
TC-U3	–	List of users, 200 OK	✅ 200 OK	None

GET /users/<user_id>
TC-U4	Valid ID	200 OK, user data	✅ 200 OK	None
TC-U5	Invalid ID	404 Not Found	✅ 404	None

PUT /users/<user_id>
TC-U6	{ "first_name": "Johnny" }	200 OK, user updated	✅ 200 OK	None
TC-U7	Invalid ID	404 Not Found	✅ 404	None

🏠 Place Endpoints
POST /places
TC-P1	Valid place + existing owner	201 Created	✅ 201 Created	None
TC-P2	Duplicate title	409 Conflict	✅ 409	None
TC-P3	Invalid owner_id	400 Owner not found	✅ 400	None

GET /places
TC-P4	–	200 OK, list of places	✅ 200 OK	None

GET /places/<place_id>
TC-P5	Valid ID	200 OK, full details (owner, amenities)	✅ 200 OK	Reviews missing
TC-P6	Invalid ID	404 Not Found	✅ 404	None

PUT /places/<place_id>
TC-P7	Valid updates	200 OK	✅ 200 OK	None
TC-P8	Invalid ID	404 Not Found	✅ 404	None

✍️ Review Endpoints
POST /reviews
TC-R1	Valid review	201 Created	✅ 201 Created	None
TC-R2	Same user & place	400 Duplicate review	✅ 400	None
TC-R3	Invalid rating (e.g., 7)	400 Invalid rating	✅ 400	None
TC-R4	Invalid user/place ID	400 Not found	✅ 400	None

GET /reviews
TC-R5	–	List of reviews, 200 OK	✅ 200 OK	None

GET /reviews/<review_id>
TC-R6	Valid ID	200 OK, review details	✅ 200 OK	None
TC-R7	Invalid ID	404 Not Found	✅ 404	None

PUT /reviews/<review_id>
TC-R8	{ "rating": 4 }	200 OK, updated	✅ 200 OK	None
TC-R9	Invalid review ID	404 Not Found	✅ 404	None

DELETE /reviews/<review_id>
TC-R10	Valid ID	200 Deleted	✅ 200 OK	None
TC-R11	Invalid ID	404 Not Found	✅ 404	None

🧱 Amenity Endpoints
POST /amenities
TC-A1	{ "name": "Wi-Fi" }	201 Created	✅ 201 Created	None
TC-A2	Duplicate name	400 Already registered	✅ 400	None

GET /amenities
TC-A3	–	List of amenities	✅ 200 OK	None

GET /amenities/<amenity_id>
TC-A4	Valid ID	200 OK, amenity data	✅ 200 OK	None
TC-A5	Invalid ID	404 Not Found	✅ 404	None

PUT /amenities/<amenity_id>
TC-A6	{ "name": "High-Speed Wi-Fi" }	200 OK	✅ 200 OK	None
TC-A7	Invalid ID	404 Not Found	✅ 404	None


-------------------------------------------------------------------------

✅ API Testing Documentation
Each test case includes the endpoint, method, input, expected output, actual result, and status (Pass/Fail). Below is the complete log of tests performed on all resources.

👤 User API
🔹 Test: Create User – Successful
Endpoint: POST /users

Input:

json
{
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@example.com"
}
Expected Output: 201 Created, user details returned with ID

Actual Output: ✅ 201 Created, user ID present

Status: ✅ Pass

🔹 Test: Create User – Duplicate Email
Endpoint: POST /users

Input: (same email as previous)

Expected Output: 400 Bad Request, error message "Email already registered"

Actual Output: ✅ 400, proper error message

Status: ✅ Pass

🔹 Test: Retrieve All Users
Endpoint: GET /users

Input: none

Expected Output: 200 OK, list of users

Actual Output: ✅ 200 OK, array returned

Status: ✅ Pass

🔹 Test: Retrieve User by ID – Not Found
Endpoint: GET /users/<invalid_id>

Input: invalid_id = "xyz"

Expected Output: 404 Not Found

Actual Output: ✅ 404, error message

Status: ✅ Pass

🏠 Place API
🔹 Test: Create Place – Valid Owner
Endpoint: POST /places

Input:

json
Copier
Modifier
{
  "title": "Ocean View",
  "description": "Near the beach",
  "price": 120.0,
  "latitude": 48.85,
  "longitude": 2.35,
  "owner_id": "existing_user_id"
}
Expected Output: 201 Created, place details returned

Actual Output: ✅ 201 Created

Status: ✅ Pass

🔹 Test: Create Place – Invalid Owner
Endpoint: POST /places

Input: owner_id: "notfound123"

Expected Output: 400 Owner not found

Actual Output: ✅ 400, error message

Status: ✅ Pass

🔹 Test: Retrieve Place by ID – With Amenities
Endpoint: GET /places/<place_id>

Expected Output: 200 OK, full place data including amenities

Actual Output: ✅ 200 OK, details returned

Status: ✅ Pass

✍️ Review API
🔹 Test: Create Review – Valid
Endpoint: POST /reviews

Input:

json
Copier
Modifier
{
  "text": "Nice place!",
  "rating": 5,
  "user_id": "existing_user",
  "place_id": "existing_place"
}
Expected Output: 201 Created

Actual Output: ✅ 201 Created

Status: ✅ Pass

🔹 Test: Create Review – Duplicate Review
Endpoint: POST /reviews (same user & place as above)

Expected Output: 400, error message "Review déjà enregistrée par cet utilisateur"

Actual Output: ✅ 400

Status: ✅ Pass

🔹 Test: Update Review – Invalid Rating
Endpoint: PUT /reviews/<id>

Input: { "rating": 7 }

Expected Output: 400, message about invalid rating range

Actual Output: ✅ 400, proper validation message

Status: ✅ Pass

🧱 Amenity API
🔹 Test: Create Amenity
Endpoint: POST /amenities

Input: { "name": "Wi-Fi" }

Expected Output: 201 Created

Actual Output: ✅ 201 Created

Status: ✅ Pass

🔹 Test: Duplicate Amenity
Endpoint: POST /amenities (name = "Wi-Fi")

Expected Output: 400, message "Amenity already registered"

Actual Output: ✅ 400

Status: ✅ Pass


