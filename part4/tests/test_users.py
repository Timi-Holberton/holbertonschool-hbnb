import unittest
from app import create_app  # ta fonction Flask factory
import json

class TestUserEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.user_ids = []

    def test_01_create_users(self):
        users = [
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@gmail.com"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@gmail.com"},
            {"first_name": "Alice", "last_name": "Wonder", "email": "alice.wonder@gmail.com"},
        ]
        for user in users:
            response = self.client.post('/api/v1/users/', json=user)
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            self.assertIn('id', data)
            self.user_ids.append(data['id'])

    def test_02_create_user_duplicate_email(self):
        user = {"first_name": "Dup", "last_name": "Email", "email": "john.doe@gmail.com"}
        response = self.client.post('/api/v1/users/', json=user)
        self.assertEqual(response.status_code, 400)

    def test_03_get_user(self):
        user_id = self.user_ids[0]
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], 'john.doe@gmail.com')

    def test_04_get_user_not_found(self):
        response = self.client.get('/api/v1/users/00000000-0000-0000-0000-000000000000')
        self.assertEqual(response.status_code, 404)

    def test_05_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

    def test_06_update_user(self):
        user_id = self.user_ids[1]
        update_data = {"first_name": "Janet", "last_name": "Doe", "email": "janet.doe@gmail.com"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Janet')
        self.assertEqual(data['email'], 'janet.doe@gmail.com')

    def test_07_update_user_not_found(self):
        update_data = {"first_name": "Ghost", "last_name": "User", "email": "ghost.user@gmail.com"}
        response = self.client.put('/api/v1/users/00000000-0000-0000-0000-000000000000', json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_08_update_user_invalid_data(self):
        user_id = self.user_ids[0]
        update_data = {"first_name": "", "last_name": "", "email": "not-an-email"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
