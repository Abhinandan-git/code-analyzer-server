import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database

def connect_database(uri: str | None = None, database_name: str = "FlaskApplication#01") -> Database:
	URI: str | None = uri or os.getenv("MONGO_URI")

	client: MongoClient = MongoClient(URI, server_api=ServerApi("1"))

	try:
		client.admin.command('ping')
	except Exception as e:
		print(e)

	return client[database_name]
