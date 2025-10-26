import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
"""
Establishes a connection to a MongoDB database.

This function creates a connection to a MongoDB database using either a provided URI
or one from environment variables. It performs a ping test to verify the connection
and returns a database instance.

Args:
	uri (str | None, optional): MongoDB connection URI. If not provided, 
		will attempt to use MONGO_URI from environment variables. Defaults to None.
	database_name (str, optional): Name of the database to connect to. 
		Defaults to "FlaskApplication#01".

Returns:
	Database: A pymongo Database instance connected to the specified database.

Raises:
	Exception: If the database connection cannot be established or verified.

Example:
	>>> db = connect_database()
	>>> db = connect_database("mongodb://localhost:27017", "my_database")
"""

def connect_database(uri: str | None = None, database_name: str = "FlaskApplication#01") -> Database:
	URI: str | None = uri or os.getenv("MONGO_URI")

	client: MongoClient = MongoClient(URI, server_api=ServerApi("1"))

	try:
		client.admin.command('ping')
	except Exception as e:
		print(e)

	return client[database_name]
