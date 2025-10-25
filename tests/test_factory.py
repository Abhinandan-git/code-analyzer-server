from tests.server_base import BaseTestCase

class TestFactory(BaseTestCase):
	def test_initial(self) -> None:
		"""Test for initial code"""
		response = self.application.get("/initial")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), {"message": "hello world"})
