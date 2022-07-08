from flask import Blueprint, jsonify

baseRoute = Blueprint("base", __name__, url_prefix="/")


@baseRoute.get("/")
def helloWorld():
    return jsonify({"message": "HelloWorld"})
