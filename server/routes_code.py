import os

from typing import Dict, Tuple, List
from flask import Blueprint, session, request
from server.utils import submit_to_database
from server.database import connect_database
"""
Flask Blueprint for code analysis functionality.
This module provides endpoints for submitting and analyzing code using Google's Generative AI.
Requires authentication for all routes.
Routes:
	/submit (GET): Submit code for analysis using Gemini AI model
Dependencies:
	- Flask
	- Google GenerativeAI client
	- Valid API key in environment variables
Functions:
	check_user(): Middleware to verify user authentication
	submit_code(): Endpoint to handle code submission and analysis
Returns:
	Tuple containing response dictionary and HTTP status code
Error Codes:
	- 401: User not authenticated
	- 400: Empty code submission
	- 503: AI model failed to generate response
"""

code_blueprint = Blueprint("code", __name__)

# Middleware to check if user is authenticated or not
@code_blueprint.before_request
def check_user() -> Tuple[Dict[str, str], int] | None:
	user_logged_in = session.get("logged_in", False)

	if not user_logged_in:
		return ({"error": "Login credentials are invalid"}, 401)
	
	return None

# Submit the code to the server
@code_blueprint.route("/submit", methods=["GET"])
def submit_code() -> Tuple[Dict[str, str], int]:
	data = request.get_json()
	code = data.get("code", "")

	if not code:
		return ({"error": "Code provided is empty"}, 400)
	
	from google import genai

	client = genai.Client(api_key=os.getenv("API_KEY", ""))
	response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=f"Analyze:\n\n{code}")

	if not response.text:
		return ({"error": "Model did not respond with any content"}, 503)
	
	database_response = submit_to_database(code, response.text)

	if database_response.get("error"):
		return ({"error": "Internal Server Error"}, 500)
	
	return ({"message": response.text, "message_id": database_response["id"]}, 200)

@code_blueprint.route("/all", methods=["GET"])
def get_codes() -> Tuple[Dict[str, List], int]:
	database = connect_database()

	user = session["user"]

	codes = database["users"].find({ "_id": user })

	return ({"codes": codes.to_list()}, 200)
