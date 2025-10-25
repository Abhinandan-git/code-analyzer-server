from flask import Blueprint
"""
Flask Blueprint module for defining API routes.

This module contains route definitions and their corresponding handler functions
for the code analyzer server.

Routes:
	/initial (GET): A test endpoint that returns a hello world message

Returns:
	Blueprint: A Flask Blueprint instance containing the defined routes
"""

routes_blueprint = Blueprint("routes", __name__)

# Initial route for testing
@routes_blueprint.route("/initial", methods=["GET"])
def hello_world() -> dict[str, str]:
	return {"message": "hello world"}
