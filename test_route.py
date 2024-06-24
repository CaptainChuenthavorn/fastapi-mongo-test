import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
#importing the FastAPI app from main.py
from main import app


client = TestClient(app)

class TestFastAPIDatabases(unittest.TestCase):
    @patch('config.database.collection_name.insert_one')
    @patch('config.database.collection_name.find_one')
    def test_create_person_success(self, mock_find_one, mock_insert_one):
        mock_find_one.return_value = None
        mock_insert_one.return_value.inserted_id = "mocked_id"
        response = client.post("/persons", json={"first_name": "John","last_name":"Doe","age":28, "email": "jogn@example.com", "phone_number": "1234567890"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Person created", response.json()["message"])

    @patch('config.database.collection_name.find_one')
    def test_create_person_duplicate(self, mock_find_one):
        mock_find_one.return_value = True
        response = client.post("/persons", json={"first_name": "John","last_name":"Doe","age":28, "email": "jogn@example.com", "phone_number": "1234567890"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email or Phone Number already exists", response.json()["detail"])

    @patch('config.database.collection_name.find')
    def test_get_all_person_success(self, mock_find):
        mock_find.return_value = [{"first_name": "John","last_name":"Doe","age":28, "email": "jogn@example.com", "phone_number": "1234567890","_id": "mocked_id", "famous": False}]
        response = client.get("/persons")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch('config.database.collection_name.find')
    def test_get_all_person_not_found(self, mock_find):
        mock_find.return_value = []
        response = client.get("/persons")
        self.assertEqual(response.status_code, 404)
        self.assertIn("No person data found", response.json()["detail"])

    @patch('config.database.collection_name.find_one')
    @patch('config.database.collection_name.delete_one')
    def test_delete_person_success(self, mock_delete_one, mock_find_one):
        mock_find_one.return_value = True
        mock_delete_one.return_value = None
        response = client.delete("/persons/667859566badd93009dd4db8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person deleted", response.json()["message"])

    # Test case for update valid person_id success
    @patch('config.database.collection_name.find_one')
    def test_update_person_success(self, mock_find_one):
        mock_find_one.side_effect = [True, False, True]  # First call for checking if person exists, second for duplicate email or phone, third for the update
        response = client.put("/persons/667859566badd93009dd4db8", json={
        "age": 30,
        "email": "captain@gmail.com",
        "famous": False,
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "0930038680"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person updated", response.json()["message"])

    # Test case for update invalid person_id
    @patch('config.database.collection_name.find_one')
    def test_update_person_unsuccess(self, mock_find_one):
        mock_find_one.side_effect = [True, False, True]  # First call for checking if person exists, second for duplicate email or phone, third for the update
        response = client.put("/persons/mocked_id", json={
        "age": 30,
        "email": "ssss@gmail.com",
        "famous": False,
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "123144567890"

        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person updated", response.json()["message"])

if __name__ == '__main__':
    unittest.main()