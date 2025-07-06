-- Table pour User
CREATE TABLE IF NOT EXISTS user (
	id CHAR(36) PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL,
	is_admin BOOLEAN DEFAULT FALSE
);

-- Table pour Place
CREATE TABLE IF NOT EXISTS place (
	id CHAR(36) PRIMARY KEY,
	title VARCHAR(255) NOT NUll,
	description TEXT,
	price DECIMAL(10, 2) NOT NULL,
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	owner_id CHAR(36),
	Foreign Key (owner_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Table pour Reviews
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

-- Table pour la liaison Place AMnetie
CREATE Table IF NOT EXISTS place_amenity(
	place_id CHAR(36),
	amenity_id CHAR(36),
	PRIMARY KEY (place_id, amenity_id),
	Foreign Key (place_id) REFERENCES places(id) ON DELETE CASCADE,
	FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Données de base

-- Administrateur avec mot de passe hacé génréréavec https://bcrypt-generator.com
INSERT INTO user(id, first_name, last_name, email, password, is_admin)
VALUES(
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	'Admin',
	'HBnB',
	'admin@hbnb.io',
	'$2a$12$MAEf7iqXk.dg2KediiYNvOHcw4DSpnjWxsOd3Xv8BAJwKrE8AHQ1O',
	TRUE
);

-- Amenities de base
INSERT INTO amenities (id, name) VALUES 
	('ec8cc2a0-a295-4a8f-b13a-b7f6c04a35f1', 'Wi-Fi'), 
	("64adf0cd-0e00-4f53-85b3-26744c8e52e2", 'Piscine'), 
	("51234158-fb59-476e-b25f-2fdaef4c32a5", "Climatisation");
