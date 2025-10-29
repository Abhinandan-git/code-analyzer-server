import unittest
import mongomock

from unittest.mock import patch
from werkzeug.security import generate_password_hash
from server import create_application

class TestCodeSubmit(unittest.TestCase):
	"""TestCodeSubmit verifies the application's code handling behaviour"""

	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.client = mongomock.MongoClient()
		self.database = self.client["FlaskApplication#01"]
		self.application = create_application({ "TESTING": True }).test_client()

		self.database.users.insert_one({ "username": "predefined", "password": generate_password_hash("password") })

	def tearDown(self) -> None:
		"""Tear down after each testcase"""
		self.client.database.users.delete_many({})

	@patch("server.routes_auth.connect_database")
	def test_user_login_fail(self, mock_connect_database) -> None:
		"""Test if unauthorized code submission fails"""
		mock_connect_database.return_value = self.database

		response = self.application.get("/code/submit")
		self.assertEqual(response.status_code, 401)

	@patch("server.routes_auth.connect_database")
	def test_code_submit_successful(self, mock_connect_database) -> None:
		"""Test if code submission is successful"""
		mock_connect_database.return_value = self.database

		self.test_code = """print('Hello World')"""

		with self.application as client:
			client.post("/login", json={"username": "predefined", "password": "password"})

			response = client.get("/code/submit", json={ "code": self.test_code })
			self.assertEqual(response.status_code, 200)
			self.assertIsNotNone(response.get_json()["message"])

	@patch("server.routes_auth.connect_database")
	def test_empty_code(self, mock_connect_database) -> None:
		"""Test if empty code fails"""
		mock_connect_database.return_value = self.database

		with self.application as client:
			client.post("/login", json={"username": "predefined", "password": "password"})

			response = client.get("/code/submit", json={"code": ""})
			self.assertEqual(response.status_code, 400)
			self.assertEqual(response.get_json()["error"], "Code provided is empty")

	@patch("server.routes_auth.connect_database")
	def test_all_codes(self, mock_connect_database) -> None:
		"""Test if all codes are fetched"""
		mock_connect_database.return_value = self.database

		with self.application as client:
			client.post("/login", json={"username": "predefined", "password": "password"})

			response = client.get("/code/all")
			self.assertEqual(response.status_code, 200)
			self.assertIsInstance(response.get_json()["codes"], list)
