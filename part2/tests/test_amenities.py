import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.amenity_ids = []

    def test_01_create_amenities(self):
        amenities = [
            {"name": "WiFi"},
            {"name": "Piscine"},
            {"name": "Parking"},
        ]
        for amenity in amenities:
            response = self.client.post('/api/v1/amenities/', json=amenity)
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIn('id', data)
            self.amenity_ids.append(data['id'])

    def test_02_create_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_03_get_amenity(self):
        amenity_id = self.amenity_ids[0]
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'WiFi')

    def test_04_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)

    def test_05_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

    def test_06_update_amenity(self):
        amenity_id = self.amenity_ids[1]
        update_data = {"name": "Climatisation"}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_07_update_amenity_not_found(self):
        response = self.client.put('/api/v1/amenities/00000000-0000-0000-0000-000000000000', json={"name": "Inexistante"})
        self.assertEqual(response.status_code, 404)

    def test_08_update_amenity_invalid(self):
        amenity_id = self.amenity_ids[0]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
