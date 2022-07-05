# 1) add CRUD operation
# 2) connect Template to operation
# demo
# @app.route("/store/customers")
# def viewCustomer():
#     dictCustomers = dbSelect(getDB(), "SELECT name, address FROM customers")
#
#     return json.dumps(dictCustomers)

from os import abort
from util.mysqlUtil import *
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']

        # insert page query
        insertRows(getDB(), "customers", ("name", "address"), [(name, address)])
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    # select pages query
    dictCustomers = dbSelect(getDB(), "SELECT name, address FROM customers")
    return render_template('datalist.html', employees=dictCustomers)


@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    # select page query
    employee = dbSelect(getDB(), "SELECT * FROM customers WHERE id = " + str(id))
    if len(employee):
        return render_template('data.html', employee=employee[0])
    return f"Employee with id ={id} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    # select page query
    employee = dbSelect(getDB(), "SELECT * FROM customers WHERE id = " + str(id))
    if request.method == 'POST':
        if len(employee):
            name = request.form['name']
            address = request.form['address']
            # update page query
            dbUpdate(getDB(), "UPDATE customers SET name = '" + name + "', address = '" + address + "' WHERE id = " + str(id))
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee[0])


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    # select page query
    employee = dbSelect(getDB(), "SELECT * FROM customers WHERE id = " + str(id))
    if request.method == 'POST':
        if employee:
            # delete page query
            dbDelete(getDB(), "DELETE FROM customers WHERE id = " + str(id))
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


app.run(host='localhost', port=5000)
