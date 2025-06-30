import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Create users for reviews with valid first_name and last_name
        cls.user_ids = []
        users = [
            {"first_name": "Alice", "last_name": "Dupont", "email": "alice.dupont@gmail.com"},
            {"first_name": "Bob", "last_name": "Martin", "email": "bob.martin@gmail.com"},
            {"first_name": "Clara", "last_name": "Durand", "email": "clara.durand@gmail.com"},
        ]
        for user in users:
            resp = cls.client.post('/api/v1/users/', json=user)
            cls.user_ids.append(resp.get_json()['id'])

        # Create one place for reviews
        cls.place_ids = []
        place_resp = cls.client.post('/api/v1/places/', json={
            "title": "Place for Reviews",
            "description": "Test place",
            "price": 60.0,
            "latitude": 40.0,
            "longitude": -70.0,
            "owner_id": cls.user_ids[0],
            "amenities": []
        })
        cls.place_ids.append(place_resp.get_json()['id'])

        cls.review_ids = []


    def test_01_create_reviews(self):
        reviews = [
            {"text": "Excellent!", "rating": 5, "user_id": self.user_ids[0], "place_id": self.place_ids[0]},
            {"text": "Pretty good", "rating": 4, "user_id": self.user_ids[1], "place_id": self.place_ids[0]},
            {"text": "Not bad", "rating": 3, "user_id": self.user_ids[2], "place_id": self.place_ids[0]},
        ]
        for review in reviews:
            response = self.client.post('/api/v1/reviews/', json=review)
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIn('id', data)
            self.review_ids.append(data['id'])

    def test_02_create_review_invalid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 10,
            "user_id": "invalid",
            "place_id": "invalid"
        })
        self.assertEqual(response.status_code, 400)

    def test_03_get_review(self):
        review_id = self.review_ids[0]
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Excellent!")

    def test_04_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)

    def test_05_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

    def test_06_update_review(self):
        review_id = self.review_ids[1]
        update_data = {"text": "Updated review", "rating": 4}
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

    def test_07_update_review_not_found(self):
        response = self.client.put('/api/v1/reviews/00000000-0000-0000-0000-000000000000', json={"text": "Ghost", "rating": 1})
        self.assertEqual(response.status_code, 404)

    def test_08_update_review_invalid(self):
        review_id = self.review_ids[0]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={"text": "", "rating": 100})
        self.assertEqual(response.status_code, 400)

    def test_09_delete_review(self):
        review_id = self.review_ids.pop()
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_10_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)

    def test_11_get_reviews_for_place(self):
        place_id = self.place_ids[0]
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

if __name__ == '__main__':
    unittest.main()
