from typing import Tuple, Dict
from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from server.database import connect_database
"""
Functions:
	hello_world() -> dict[str, str]:
		Test endpoint that returns a hello world message.
			dict: A dictionary containing a hello message.
	register_user() -> Tuple[Dict[str, str], int]:
		Handles user registration by storing username and hashed password in database.
			tuple: A tuple containing response message and HTTP status code.
			Response codes:
				201: User registered successfully
				400: Missing username or password
				409: Username already exists
	login_user() -> Tuple[Dict[str, str], int]:
		Authenticates user credentials and creates a session.
			tuple: A tuple containing response message and HTTP status code.
			Response codes:
				200: User logged in successfully
				400: Missing username or password
				401: Incorrect password
				404: User does not exist
	logout() -> Dict[str, str]:
		Clears user session.
			dict: A dictionary containing logout confirmation message.
	load_user_session() -> Tuple[Dict[str, str], int]:
		Middleware that checks user authentication status before each request.
			tuple: A tuple containing response message and HTTP status code.
			Response codes:
				200: User is logged in
				401: User is not logged in
Note:
	All routes return JSON responses with appropriate HTTP status codes.
	Session management is handled using Flask's session object.
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

	session["user"] = str(user["_id"])
	session["logged_in"] = True
	return ({"message": "User login successfully"}, 200)

# Route for logging out
@routes_blueprint.route("/logout", methods=["GET", "POST"])
def logout() -> Dict[str, str]:
	session.clear()
	return {"message": "Logged out successfully"}
