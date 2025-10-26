import unittest

from server.database import connect_database
from server import create_application
from server.routes import session
from unittest.mock import patch
from werkzeug.security import generate_password_hash

class TestAuthIntegration(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		"""Setup before each test instance"""
		cls.database = connect_database(database_name="TestFlaskApplication")
		cls.application = create_application({ "TESTING": True }).test_client()

	@classmethod
	def tearDownClass(cls) -> None:
		"""Tear down after each test instance"""
		cls.database.client.drop_database("TestFlaskApplication")

	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.database.users.insert_one({ "username": "integration_predefined", "password": generate_password_hash("password") })

	def tearDown(self) -> None:
		"""Tear down before each testcase"""
		self.database.users.delete_many({})

	@patch("server.routes.connect_database")
	def test_register_login_successful_flow(self, mock_connect_database) -> None:
		"""Test successful register and login of a user"""
		mock_connect_database.return_value = self.database

		register = self.application.post("/register", json={
			"username": "integration_username",
			"password": "integration_password"
		})
		self.assertEqual(register.status_code, 201)

		user = self.database.users.find_one({ "username": "integration_username" })
		self.assertIsNotNone(user)

		login = self.application.post("/login", json={
			"username": "integration_username",
			"password": "integration_password"
		})
		self.assertEqual(login.status_code, 200)

		with self.application as client:
			client.post("/login", json={ "username": "integration_username", "password": "integration_password" })

			self.assertTrue(session.get("logged_in"))
			self.assertIsNotNone(session.get("user"))
