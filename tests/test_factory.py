<<<<<<< HEAD
import unittest
from server import create_application

class TestApplication(unittest.TestCase):
	"""TestApplication verifies the application's basic startup behavior.

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
=======
from tests.server_base import BaseTestCase

class TestFactory(BaseTestCase):
	def test_initial(self) -> None:
		"""Test for initial code"""
		if self.application:
			response = self.application.get("/initial")
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.get_json(), {"message": "hello world"})
>>>>>>> a0f3822b470549830a85d546992eeca23628b250
