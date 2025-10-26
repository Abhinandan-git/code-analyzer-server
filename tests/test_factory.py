import unittest

from server import create_application

class TestFactory(unittest.TestCase):
	"""TestFactory verifies the application's basic startup behavior.

	Asserts that a GET request to the "/initial" endpoint returns the expected JSON payload
	{"message": "hello world"}.
	"""

	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.application = create_application({ "TESTING": True }).test_client()

	def tearDown(self) -> None:
		"""Tear down after each testcase"""
		self.application = None

	def test_initial(self) -> None:
		"""Test for initial code"""
		if self.application:
			response = self.application.get("/initial")
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.get_json(), {"message": "hello world"})
