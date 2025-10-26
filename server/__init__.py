import os

from flask import Flask
from typing import Optional, Mapping, Any

def create_application(test_configuration: Optional[Mapping[str, Any]] = None) -> Flask:
	"""
	Create and configure and return a Flask application instance.
	Parameters
	----------
	test_configuration : Optional[Mapping] or None
		If provided, this mapping is loaded into the application's configuration
		using Flask.config.from_mapping(), which is useful for tests to supply
		deterministic settings. If None, the application will attempt to load
		configuration from the instance file "config.py" via
		Flask.config.from_pyfile("config.py", silent=True). Both loading paths use
		silent=True so missing files or keys do not raise errors.
	Returns
	-------
	Flask
		A configured Flask application. The returned application has:
		- instance_relative_config set to True,
		- its instance folder created on disk (os.makedirs(..., exist_ok=True)),
		- a simple test route registered at "/initial" that returns {"message": "hello world"}.
	Side effects
	------------
	- Ensures the application's instance folder exists by creating it if necessary.
	- Registers a lightweight "/initial" route useful for smoke tests.
	Notes
	-----
	- The function assumes Flask (and os) are available/imported in the module.
	- Prefer passing a test_configuration mapping in tests to avoid depending on
		environment-specific instance configuration files.
	"""
	
	# Create and configure the application
	application: Flask = Flask(__name__, instance_relative_config=True)
	application.secret_key = os.getenv("SECRET_KEY") or ""

	if test_configuration is not None:
		application.config.from_mapping(test_configuration, silent=True)
	
	# Ensure the instance folder exists
	os.makedirs(application.instance_path, exist_ok=True)
	
	from .routes import routes_blueprint

	application.register_blueprint(routes_blueprint, url_prefix="/")
	
	return application
