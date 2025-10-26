import unittest

from typing import Any
from server.database import connect_database

class DatabaseTestCase(unittest.TestCase):
	def setUp(self) -> None:
		"""Setup before each testcase"""
		self.database = connect_database()
	
	def tearDown(self) -> None:
		"""Tear down after each testcase"""
		self.database.test_collection.delete_many({})
		self.database.client.close()

	def test_check_instance(self) -> None:
		"""Test if MongoDB instance is initialized and connected"""
		self.assertIsNotNone(self.database, "MongoDB instance should be initialized")
		
		collections = self.database.list_collection_names()
		self.assertIsInstance(collections, list)

	def test_insert_document(self) -> None:
		"""Test if insert and retrieval work"""
		self.database.test_collection.insert_one({ "message": "unittest check" })

		response: dict[str, Any] | None = self.database.test_collection.find_one({ "message": "unittest check" })
		self.assertIsNotNone(response)
		if response:
			self.assertEqual(response.get("message"), "unittest check")
