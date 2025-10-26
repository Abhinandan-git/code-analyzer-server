import unittest
import mongomock

from werkzeug.security import generate_password_hash
from server import create_application
from unittest.mock import patch

class TestAuth(unittest.TestCase):
	"""TestAuth verifies the application's authentication behaviour.

	Asserts that a POST request to the "/register" enpoint returns valid errors
	and expected JSON payload.
	"""

	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.client = mongomock.MongoClient()
		self.database = self.client["FlaskApplication#01"]
		self.application = create_application({ "TESTING": True }).test_client()

		self.database.users.insert_one({ "username": "predefined", "password": generate_password_hash("password") })

	def tearDown(self) -> None:
		"""Tear down after each testcase"""
		self.client.database.users.delete_many({})

	@patch("server.routes.connect_database")
	def test_register_user_success(self, mock_connect_database) -> None:
		"""Test new user registration"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/register", json={ "username": "test", "password": "password" })

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json()["message"], "User registered successfully")

		self.assertIsNotNone(self.database.users.find_one({"username": "test"}))

	@patch("server.routes.connect_database")
	def test_register_user_incomplete(self, mock_connect_database) -> None:
		"""Test incomplete user registeration"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/register", json={ "username": "predefined" })
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"], "Missing username or password")
		
		response = self.application.post("/register", json={ "password": "password" })
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"], "Missing username or password")

	@patch("server.routes.connect_database")
	def test_register_user_existing(self, mock_connect_database) -> None:
		"""Test existing user registeration error"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/register", json={ "username": "predefined", "password": "password" })
		self.assertEqual(response.status_code, 409)
		self.assertEqual(response.get_json()["error"], "Username already exists")

	@patch("server.routes.connect_database")
	def test_login_user_successfully(self, mock_connect_database) -> None:
		"""Test existing user login"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/login", json={ "username": "predefined", "password": "password" })
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json()["message"], "User login successfully")

	@patch("server.routes.connect_database")
	def test_login_user_incomplete(self, mock_connect_database) -> None:
		"""Test incomplete user login"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/login", json={ "username": "predefined" })
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"], "Missing username or password")

		response = self.application.post("/login", json={ "password": "password" })
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json()["error"], "Missing username or password")

	@patch("server.routes.connect_database")
	def test_login_user_incorrect_password(self, mock_connect_database) -> None:
		"""Test inccorect user login"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/login", json={ "username": "predefined", "password": "wrong_password" })
		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.get_json()["error"], "Incorrect password")

	@patch("server.routes.connect_database")
	def test_login_user_incorrect_username(self, mock_connect_database) -> None:
		"""Test inccorect user login"""
		mock_connect_database.return_value = self.database

		response = self.application.post("/login", json={ "username": "wrong_username", "password": "password" })
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json()["error"], "User does not exist")
