import json
from flask import Flask, render_template, request, make_response
from util.mysqlUtil import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route("/store/customers")
def viewCustomer():
    dictCustomers = dbSelect(getDB(), "SELECT name, address FROM customers")

    return json.dumps(dictCustomers)

if __name__ == '__main__':
    app.run(debug=True)
