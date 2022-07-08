import json
import validators

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.util.mysqlUtil import *
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

# define the root path
customersRoute = Blueprint("customers", __name__, url_prefix="/api/customers")

# define connection
db = getDB()


# define routes
@customersRoute.get("/")
def getAll():
    customers = dbSelect(db, "SELECT * FROM customers")
    keyList = ["id", "name", "address"]
    res = []
    for customer in customers:
        customerDict = {}
        for i, key in enumerate(keyList):
            customerDict[key] = customer[i]
        res.append(customerDict)

    return jsonify(res), 200


@customersRoute.get("/<int:customerID>")
def getCustomer(customerID):
    customers = dbSelect(db, "SELECT * FROM customers WHERE id = " + str(customerID))
    if not len(customers):
        return {"message": "Not found"}, 404
    customer = customers[0]
    return jsonify({'id': customer[0], 'name': customer[1], 'address': customer[2]}), 200


@customersRoute.post("/")
def createCustomer():
    name = request.json['name']
    address = request.json['address']

    # password_hash = generate_password_hash(password)
    insertRows(db, "customers", ("name", "address"), [(name, address)])
    return jsonify({"message": "User created"}), 201


@customersRoute.delete("/<int:customerID>")
def deleteCustomer(customerID):
    customer = dbSelect(db, "SELECT * FROM customers WHERE id = " + str(customerID))
    if not len(customer):
        return {"message": "Not found"}, 404
    dbDelete(db, "DELETE FROM customers WHERE id = " + str(customerID))
    return jsonify({"result": True}, 200)


@customersRoute.put("/<int:customerID>")
def updateCustomer(customerID):
    name = request.json['name']
    address = request.json['address']

    customer = dbSelect(db, "SELECT * FROM customers WHERE id = " + str(customerID))
    if not len(customer):
        return {"message": "Not found"}, 404
    dbUpdate(db,
             "UPDATE customers SET name = '" + name + "', address = '" + address + "' WHERE id = " + str(customerID))
    return (jsonify({
        'name': name,
        'address': address,
    }), 200)
