import unittest

from server import create_application

class BaseTestCase(unittest.TestCase):
	"""BaseTestCase verifies the application's basic startup behavior.

	Asserts that a
	GET request to the "/initial" endpoint returns the expected JSON payload
	{"message": "hello world"}.
	"""

	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.application = create_application({ "TESTING": True }).test_client()

	def tearDown(self) -> None:
		"""Tear down after each testcase"""
		del self.application
