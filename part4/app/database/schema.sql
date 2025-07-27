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

-- Liaisons amenities-places avec les UUIDs ci-dessus
-- Minas Tirith
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', '11111111-1111-1111-1111-111111111111'),
  ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', '22222222-2222-2222-2222-222222222222'),
  ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', '33333333-3333-3333-3333-333333333333'),
  ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', '44444444-4444-4444-4444-444444444444'),
  ('c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', '55555555-5555-5555-5555-555555555555');

-- Helm's Deep
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('1aa301e0-3cc9-4a3a-804c-84cfcd034181', '66666666-6666-6666-6666-666666666666'),
  ('1aa301e0-3cc9-4a3a-804c-84cfcd034181', '77777777-7777-7777-7777-777777777777'),
  ('1aa301e0-3cc9-4a3a-804c-84cfcd034181', '88888888-8888-8888-8888-888888888888'),
  ('1aa301e0-3cc9-4a3a-804c-84cfcd034181', '99999999-9999-9999-9999-999999999999'),
  ('1aa301e0-3cc9-4a3a-804c-84cfcd034181', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa');

-- Fondcombe
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'),
  ('b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', 'cccccccc-cccc-cccc-cccc-cccccccccccc'),
  ('b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', 'dddddddd-dddd-dddd-dddd-dddddddddddd'),
  ('b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee'),
  ('b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', 'ffffffff-ffff-ffff-ffff-ffffffffffff');

-- Mordor
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('d34f9f4d-2bf5-4623-b7f4-888d33c48e33', '123e4567-e89b-12d3-a456-426614174000'),
  ('d34f9f4d-2bf5-4623-b7f4-888d33c48e33', '223e4567-e89b-12d3-a456-426614174001'),
  ('d34f9f4d-2bf5-4623-b7f4-888d33c48e33', '323e4567-e89b-12d3-a456-426614174002'),
  ('d34f9f4d-2bf5-4623-b7f4-888d33c48e33', '423e4567-e89b-12d3-a456-426614174003'),
  ('d34f9f4d-2bf5-4623-b7f4-888d33c48e33', '523e4567-e89b-12d3-a456-426614174004');

-- Mines of Moria
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('f9305b02-c7a9-4c85-88ff-d40a7382cba9', '623e4567-e89b-12d3-a456-426614174005'),
  ('f9305b02-c7a9-4c85-88ff-d40a7382cba9', '723e4567-e89b-12d3-a456-426614174006'),
  ('f9305b02-c7a9-4c85-88ff-d40a7382cba9', '823e4567-e89b-12d3-a456-426614174007'),
  ('f9305b02-c7a9-4c85-88ff-d40a7382cba9', '923e4567-e89b-12d3-a456-426614174008'),
  ('f9305b02-c7a9-4c85-88ff-d40a7382cba9', 'a23e4567-e89b-12d3-a456-426614174009');

-- The Prancing Pony
INSERT INTO place_amenity (place_id, amenity_id) VALUES
  ('ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', 'b23e4567-e89b-12d3-a456-426614174010'),
  ('ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', 'c23e4567-e89b-12d3-a456-426614174011'),
  ('ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', 'd23e4567-e89b-12d3-a456-426614174012'),
  ('ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', 'e23e4567-e89b-12d3-a456-426614174013'),
  ('ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', 'f23e4567-e89b-12d3-a456-426614174014');

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
	'Boromir',
	'Toujours Debout',
	'boromir@gmail.com',
	'$2y$10$CuuDSEJWnbggMTn5YH0EnuTqLJNVI0d1HQ1TB4gwdh4LmzBMMrSMG',
	FALSE,
	datetime('now')
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at)
VALUES(
	'3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1',
	'Sam',
	'Le Brave',
	'samlebrave@gmail.com',
	'$2y$10$SIkt7/eo7TBwEieOxJ4yKebGovfY5oQUietpuKX7u/Ogmk4IAdWya',
	FALSE,
	datetime('now')
);


-- INSERT for amenities Table
INSERT INTO amenities (id, name, created_at) VALUES
	('11111111-1111-1111-1111-111111111111', 'Panoramic anti-orc balcony', datetime('now')),
	('22222222-2222-2222-2222-222222222222', '100% natural cardio stairs', datetime('now')),
	('33333333-3333-3333-3333-333333333333', 'Emergency bell (crisis included)', datetime('now')),
	('44444444-4444-4444-4444-444444444444', 'Wi-Fi launched straight from Osgiliath', datetime('now')),
	('55555555-5555-5555-5555-555555555555', 'Nazgûl-proof certified stone wall', datetime('now')),
	('66666666-6666-6666-6666-666666666666', 'Vaulted halls with almost soundproofing', datetime('now')),
	('77777777-7777-7777-7777-777777777777', 'Elf launch ramp (limited use)', datetime('now')),
	('88888888-8888-8888-8888-888888888888', 'Optional troll cistern', datetime('now')),
	('99999999-9999-9999-9999-999999999999', 'Built-in rainstorm during attacks', datetime('now')),
	('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Emergency cave-based exit system', datetime('now')),
	('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Zen fountain with existential reflections', datetime('now')),
	('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Self-service harpists', datetime('now')),
	('dddddddd-dddd-dddd-dddd-dddddddddddd', 'Elven library (endless scrolls included)', datetime('now')),
	('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'Natural light filtered by ancient wisdom', datetime('now')),
	('ffffffff-ffff-ffff-ffff-ffffffffffff', 'Beds that recite Lórien poetry at night', datetime('now')),
	('123e4567-e89b-12d3-a456-426614174000', 'Direct view of Mount Doom (heating included)', datetime('now')),
	('223e4567-e89b-12d3-a456-426614174001', '24/7 giant flaming eye surveillance', datetime('now')),
	('323e4567-e89b-12d3-a456-426614174002', 'Grass-free guaranteed lava floors', datetime('now')),
	('423e4567-e89b-12d3-a456-426614174003', 'Unfiltered sulfur-rich air', datetime('now')),
	('523e4567-e89b-12d3-a456-426614174004', 'Express mail service via Nazgûl', datetime('now')),
	('623e4567-e89b-12d3-a456-426614174005', '10 km² grand entrance hall', datetime('now')),
	('723e4567-e89b-12d3-a456-426614174006', 'Pet Balrog (not house-trained)', datetime('now')),
	('823e4567-e89b-12d3-a456-426614174007', 'Deep drums in surround sound™', datetime('now')),
	('923e4567-e89b-12d3-a456-426614174008', 'Broken bridge (members only)', datetime('now')),
	('a23e4567-e89b-12d3-a456-426614174009', 'Random staircases (no exit guaranteed)', datetime('now')),
	('b23e4567-e89b-12d3-a456-426614174010', 'Unlimited semi-cold ale', datetime('now')),
	('c23e4567-e89b-12d3-a456-426614174011', 'Hobbit songs at sunset', datetime('now')),
	('d23e4567-e89b-12d3-a456-426614174012', 'Authentic squeaky wooden locks', datetime('now')),
	('e23e4567-e89b-12d3-a456-426614174013', 'Guests: 50% mysterious, 50% drunk', datetime('now')),
	('f23e4567-e89b-12d3-a456-426614174014', 'Unattended pony parking out back', datetime('now'));

-- INSERT for places Table
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES(
	'c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2',
	'Minas Tirith',
	'7 floors, no elevator, but a breathtaking view of the battles! Perfect for lovers of white stone, dramatic balconies, and orc neighbors that get a little too close.',
	120,
	-59,
	89,
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	datetime('now')
);

-- Gouffre de Helm
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES(
	'1aa301e0-3cc9-4a3a-804c-84cfcd034181',
	'Gouffre de Helm',
	'The perfect getaway if you like cold stone, tight spaces, and the thrill of imminent invasion. Thick walls, natural air conditioning, and complimentary catapult service. Ideal for cozy nights with 10,000 screaming Uruk-hai. Bonus: spacious cave in case of emergency exit.',
	50,
	-15,
	67,
	'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
	datetime('now')
);

-- Fondcombe
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES (
    'b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111',
    'Fondcombe',
    'An upscale Elvish retreat, perfect for lovers of cryptic poetry, 24/7 harp concerts, and slow-motion stair walks. The ideal place to heal your wounds… or avoid your problems. Warning: high risk of philosophical monologues.',
    100,
    45,
    6,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    datetime('now')
);

-- Mordor
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES (
    'd34f9f4d-2bf5-4623-b7f4-888d33c48e33',
    'Mordor',
    'A volcanic hotspot for fans of extreme heat, barren landscapes, and being constantly watched by a giant flaming eye. No sunlight, guaranteed toxic vibes. Perfect for introverts… and megalomaniac overlords.',
    10,
    -10,
    80,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    datetime('now')
);

-- Mines of Moria
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES (
    'f9305b02-c7a9-4c85-88ff-d40a7382cba9',
    'Mines of Moria',
    'Once a luxury mine, now a full-scale escape room experience. Ideal for echo lovers, creepy corridors, and things you really shouldn’t wake up. Comes with dust, darkness, and complimentary drums of doom.',
    70,
    -40,
    50,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    datetime('now')
);

-- The Prancing Pony
INSERT INTO places (id, title, description, _price, _latitude, _longitude, owner_id, created_at)
VALUES (
    'ee41ad7e-d2ce-46f1-8d0b-1fb183f73844',
    'The Prancing Pony',
    'Rustic charm in the heart of Bree. Warm ales, loud bards, and paper-thin walls. Great for laying low while on the run from Ringwraiths (black cloak not included).',
    80,
    10,
    30,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    datetime('now')
);


-- INSERT for reviews Table
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at) VALUES
	('a1b2c3d4-1111-2222-3333-444455556666', 'Great stay at Minas Tirith! Between the 7 floors with no elevator and orcs screaming downstairs, I got in shape… and so did my screams! The panoramic balcony is perfect for watching battles, but avoid the Wi-Fi—it’s faster to send a raven. Would definitely do it again (with good sneakers)!', 4, 'e9cb3581-7058-4c12-9c73-3d3fe56c06e8', 'c1a4b9de-7fcb-4df4-89c7-9a7f62c5f3b2', datetime('now')),
	('b2c3d4e5-2222-3333-4444-555566667777', 'Helm’s Deep was the ultimate survival challenge! Thick walls, nonstop Uruk-hai screams, and the complimentary rain made it feel like home. Just don’t ask about the catapult service—it’s more of a “you’re on your own” kind of thing.', 2, '3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1', '1aa301e0-3cc9-4a3a-804c-84cfcd034181', datetime('now')),
	('c3d4e5f6-3333-4444-5555-666677778888', 'Foncombe is lovely if you enjoy endless harp music and cryptic poetry that makes your head spin. The beds sing poems, which is cool… until you want to sleep. A great place to run away from your problems, or your relatives.', 4, '3e2a1b40-9d9f-4c6b-a2db-8e4f12e645a1', 'b1e2a7c3-1dcd-41ea-9e2f-f1b4d4a5a111', datetime('now')),
	('d4e5f6g7-4444-5555-6666-777788889999', 'Mordor’s heating system is top-notch (lava everywhere!), but the air quality? Not so much. The giant flaming eye is an interesting touch, but privacy is definitely not a thing here. Perfect for introverts who don’t mind a little apocalypse.', 1, 'e9cb3581-7058-4c12-9c73-3d3fe56c06e8', 'd34f9f4d-2bf5-4623-b7f4-888d33c48e33', datetime('now')),
	('e5f6g7h8-5555-6666-7777-888899990000', 'Moria is the place if you love echo, darkness, and surprise appearances by shadowy creatures. The pet Balrog isn’t exactly friendly, and the stairs keep you guessing. Not for the faint-hearted—but great for thrill seekers!', 2, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'f9305b02-c7a9-4c85-88ff-d40a7382cba9', datetime('now')),
	('f6g7h8i9-6666-7777-8888-999900001111', 'The Prancing Pony has charm and ale in abundance, though the walls are as thin as paper. Perfect for loud nights and mysterious guests. Just don’t expect a quiet stay if the hobbits get singing!', 3, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'ee41ad7e-d2ce-46f1-8d0b-1fb183f73844', datetime('now'));

-- Select for some tables
SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;

