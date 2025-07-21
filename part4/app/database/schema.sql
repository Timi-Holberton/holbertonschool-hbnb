-- Table pour users
CREATE TABLE IF NOT EXISTS users (
	id CHAR(36) PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE
);


-- Table pour places
CREATE TABLE IF NOT EXISTS places (
	id CHAR(36) PRIMARY KEY,
	title VARCHAR(255) NOT NUll,
	description TEXT,
	_price DECIMAL(10, 2) NOT NULL,
	_latitude FLOAT NOT NULL,
	_longitude FLOAT NOT NULL,
	owner_id CHAR(36),
	Foreign Key (owner_id) REFERENCES users(id) ON DELETE CASCADE
);


-- Table pour reviews
CREATE TABLE IF NOT EXISTS reviews (
	id CHAR(36) PRIMARY KEY,
	text TEXT NOT NULL,
	rating INT CHECK (rating BETWEEN 1 AND 5),
	user_id CHAR(36) NOT NULL,
	place_id CHAR(36) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
	FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
	UNIQUE (user_id, place_id)
);


-- Table pour Amenities
CREATE TABLE IF NOT EXISTS amenities (
	id CHAR(36) PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL
);


-- Table pour la liaison places Amenitie
CREATE TABLE IF NOT EXISTS place_amenity (
	place_id CHAR(36),
	amenity_id CHAR(36),
	PRIMARY KEY (place_id, amenity_id),
	Foreign Key (place_id) REFERENCES places(id) ON DELETE CASCADE,
	FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- INSERT for places_amenity Table
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', 'ec8cc2a0-a295-4a8f-b13a-b7f6c04a35f1');

-- INSERT for users Table
-- users de base (Administrateur avec mot de passe hacé génréré avec https://bcrypt-generator.com)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at)
VALUES(
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	'Admin',
	'HBnB',
	'admin@hbnb.io',
	'$2a$12$MAEf7iqXk.dg2KediiYNvOHcw4DSpnjWxsOd3Xv8BAJwKrE8AHQ1O',
	TRUE,
	datetime('now')
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at)
VALUES(
	'e9cb3581-7058-4c12-9c73-3d3fe56c06e8',
	'Test-users',
	'A supprimer',
	'test-usersasupprimer@gmail.com',
	'$2a$12$L0n.fHHrJdIydlge4yhzOOJDr9HSz/LvI7GzS.ke4gpn/3uj.kCbG',
	FALSE,
	datetime('now')
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at)
VALUES(
	'3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1',
	'users-update',
	'holberton',
	'holberton@gmail.com',
	'$2a$12$4pHCLukTh30/W6LAJJn/O.dZosp7.u0DSWqmhX2lKbyQkTWfiSTBO',
	FALSE,
	datetime('now')
);


-- INSERT for amenities Table
INSERT INTO amenities (id, name, created_at) VALUES 
	('ec8cc2a0-a295-4a8f-b13a-b7f6c04a35f1', 'Wi-Fi', datetime('now')), 
	('64adf0cd-0e00-4f53-85b3-26744c8e52e2', 'Piscine', datetime('now')), 
	('51234158-fb59-476e-b25f-2fdaef4c32a5', 'Climatisation', datetime('now')),
	('2f3b62b8-c01d-4a6e-9fe2-c3c1d6f601d7', 'Vieille Télévision à changer', datetime('now')),
	('8b0a9e13-4de6-41f4-86bb-cde4d68b6e6b', 'Cafetière cassé à supprimer', datetime('now'));

-- INSERT for places Table
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES(
	'c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2',
	'Minas Tirith',
	'La cité blanche accueille seulement les fidèles du Gondor',
	10000,
	-59,
	89,
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	datetime('now')
);

INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES(
	'5de9fca1-2e2b-4e32-bc94-1ec4cc6eeb7d',
	'Mordor',
	'Terre stérile à supprimer',
	1,
	-23,
	-45,
	'3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1',
	datetime('now')
);

INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES(
	'1aa301e0-3cc9-4a3a-804c-84cfcd034181',
	'Gouffre de Helm',
	'Besoin de travaux après bataille',
	100,
	-15,
	67,
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	datetime('now')
);


-- INSERT for reviews Table
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at)
VALUES(
	'3c4e2c9d-1b80-4023-9f9b-d7b3d238de70',
	'Splendide arbre blanc en fleur',
	5,
	'e9cb3581-7058-4c12-9c73-3d3fe56c06e8',
	'c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2',
	datetime('now')
);

INSERT INTO reviews (id, text, rating, user_id, place_id, created_at)
VALUES(
	'd7bcd4e0-df8f-4f77-9d7e-8a3de99fa624',
	'Très très moche, je suis épiée par un oeil énorme, à fuir !!',
	1,
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	'5de9fca1-2e2b-4e32-bc94-1ec4cc6eeb7d',
	datetime('now')
);

INSERT INTO reviews (id, text, rating, user_id, place_id, created_at)
VALUES(
	'6e329857-52ae-4f6c-ae1a-0ef7b87df181',
	"Beaucoup de poussière et des cadavres un peu partout, ce n'est pas très propre",
	3,
	'3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1',
	'1aa301e0-3cc9-4a3a-804c-84cfcd034181',
	datetime('now')
);


-- Select for some tables
SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;


-- UPDATE for some tables
UPDATE users
SET first_name = 'Isildur',
	updated_at = CURRENT_TIMESTAMP
WHERE last_name = 'holberton';

UPDATE places
SET description = 'Les travaux sont terminés',
	updated_at = CURRENT_TIMESTAMP
WHERE title = 'Gouffre de Helm';

UPDATE amenities
SET name = 'Télévision nouvelle',
	updated_at = CURRENT_TIMESTAMP
WHERE id = '2f3b62b8-c01d-4a6e-9fe2-c3c1d6f601d7';

UPDATE reviews
SET text = 'à fuir !!',
	updated_at = CURRENT_TIMESTAMP
WHERE rating = 3;


-- Delete for some tables
DELETE FROM reviews WHERE rating = 1;
DELETE FROM amenities WHERE name = 'Cafetière cassé à supprimer';
DELETE FROM places WHERE title = 'Mordor';
DELETE FROM users WHERE last_name = 'A supprimer';
