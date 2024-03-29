from flask_jwt_extended import JWTManager

# from route.customers import customersRoute
from route.helloWorld import baseRoute
from flask_cors import CORS
from flask import Flask
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
    # app.register_blueprint(customersRoute)
    app.register_blueprint(baseRoute)

    return app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app = create_app()
    app.run(host='0.0.0.0',port=port)