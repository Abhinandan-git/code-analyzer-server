import unittest
from flask.testing import FlaskClient
from server import create_application

class TestApplication(unittest.TestCase):
	"""InitialTestCase verifies the application's basic startup behavior.

	Asserts that a
	GET request to the "/initial" endpoint returns the expected JSON payload
	{"message": "hello world"}.
	"""

	def setUp(self):
		"""Setup before each testcase"""
		self.application = create_application({ "TESTING": True }).test_client()

	def tearDown(self):
		"""Tear down after each testcase"""
		del self.application

	def test_initial(self):
		"""Test for initial code"""
		self.assertEqual(self.application.get("/initial").get_json(), {"message": "hello world"})
