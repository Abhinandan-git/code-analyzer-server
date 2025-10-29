from server.database import connect_database
from typing import Dict
from flask import session

def submit_to_database(code: str, response: str) -> Dict[str, str]:
	database = connect_database()

	insert_response = database["codes"].insert_one({ "code": code, "response": response, "user": session["user"] })

	if not insert_response.acknowledged:
		return {"error": "Database failed to insert the record"}

	return {"id": str(insert_response.inserted_id)}
