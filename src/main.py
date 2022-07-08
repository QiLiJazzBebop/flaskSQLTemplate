from flask_jwt_extended import JWTManager

from src.route.customers import customersRoute
from src.route.helloWorld import baseRoute
from flask_cors import CORS
from flask import Flask, config, redirect
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    # Init JWT for this application
    JWTManager(app)

    # Registering endpoints
    app.register_blueprint(customersRoute)
    app.register_blueprint(baseRoute)

    return app