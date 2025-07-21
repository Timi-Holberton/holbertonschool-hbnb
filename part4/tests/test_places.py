import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.user_ids = []
        cls.amenity_ids = []
        cls.place_ids = []

        # Créer 1 user minimal pour owner_id
        user_resp = cls.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner.user@gmail.com"
        })
        cls.user_ids.append(user_resp.get_json()['id'])

        # Créer 2 amenities pour tester la relation amenities
        for name in ["WiFi", "Parking"]:
            resp = cls.client.post('/api/v1/amenities/', json={"name": name})
            cls.amenity_ids.append(resp.get_json()['id'])

    def test_01_create_places(self):
        places = [
            {
                "title": "Chez Timi",
                "description": "la totale en campagne",
                "price": 50.0,
                "latitude": 60,
                "longitude": 25,
                "owner_id": self.user_ids[0],
                "amenities": self.amenity_ids
            },
            {
                "title": "Appartement cosy",
                "description": "En plein centre-ville",
                "price": 75.0,
                "latitude": 48,
                "longitude": 2,
                "owner_id": self.user_ids[0],
                "amenities": [self.amenity_ids[0]]
            },
            {
                "title": "Studio urbain",
                "description": "Pratique et moderne",
                "price": 65.0,
                "latitude": 48.85,
                "longitude": 2.35,
                "owner_id": self.user_ids[0],
                "amenities": []
            }
        ]
        for place in places:
            response = self.client.post('/api/v1/places/', json=place)
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIn('id', data)
            self.place_ids.append(data['id'])

    def test_02_create_place_invalid(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -10,
            "latitude": 1000,
            "longitude": 1000,
            "owner_id": "invalid-owner-id",
            "amenities": ["invalid-amenity-id"]
        })
        self.assertEqual(response.status_code, 400)

    def test_03_get_place(self):
        place_id = self.place_ids[0]
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Chez Timi")
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_04_get_place_not_found(self):
        response = self.client.get('/api/v1/places/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)

    def test_05_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

    def test_06_update_place(self):
        place_id = self.place_ids[1]
        update_data = {
            "title": "Appartement rénové",
            "description": "Tout neuf et confortable",
            "price": 80.0
        }
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_07_update_place_not_found(self):
        response = self.client.put('/api/v1/places/00000000-0000-0000-0000-000000000000', json={
            "title": "Inexistant"
        })
        self.assertEqual(response.status_code, 404)

    def test_08_update_place_invalid(self):
        place_id = self.place_ids[0]
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": -100
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
