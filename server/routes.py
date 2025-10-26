from typing import Tuple, Dict
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from server.database import connect_database
"""
Flask Blueprint module for defining API routes.

This module contains route definitions and their corresponding handler functions
for the code analyzer server.

Routes:
	/initial (GET): A test endpoint that returns a hello world message
	/register (POST): Registering endpoint that returns session

Returns:
	Blueprint: A Flask Blueprint instance containing the defined routes
"""

routes_blueprint = Blueprint("routes", __name__)

# Initial route for testing
@routes_blueprint.route("/initial", methods=["GET"])
def hello_world() -> dict[str, str]:
	return {"message": "hello world"}

# Route for registering a user
@routes_blueprint.route("/register", methods=["POST"])
def register_user() -> Tuple[Dict[str, str], int]:
	database = connect_database()

	data = request.get_json()
	username = data.get("username")
	password = data.get("password")

	if not username or not password:
		return ({"error": "Missing username or password"}, 400)

	if database["users"].find_one({ "username": username }):
		return ({"error": "Username already exists"}, 409)

	hashed_pw = generate_password_hash(password)
	database["users"].insert_one({ "username": username, "password": hashed_pw })
	return ({"message": "User registered successfully"}, 201)

# Route for user login
@routes_blueprint.route("/login", methods=["POST"])
def login_user() -> Tuple[Dict[str, str], int]:
	database = connect_database()

	data = request.get_json()
	username = data.get("username")
	password = data.get("password")

	if not username or not password:
		return ({"error": "Missing username or password"}, 400)

	user = database["users"].find_one({"username": username})
	if not user:
		return ({"error": "User does not exist"}, 404)

	if not check_password_hash(user.get("password"), password):
		return ({"error": "Incorrect password"}, 401)

	return ({"message": "User login successfully"}, 200)
