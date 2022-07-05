
from mysqlUtil import *

"""
test area
"""
# database create test
createDatabase(getDBServer(), "envTestDatabase")

# database drop test
dropDatabase(getDBServer(), "envTestDatabase")

# table create test
createTableSpecified(getDB(), "customers2", ["id INT AUTO_INCREMENT PRIMARY KEY",
                                             "name VARCHAR(255)",
                                             "address VARCHAR(255)"])

# table drop test
dropTable(getDB(), "customers2")

# insert test
keyTupleDemo = ("name", "address")
valueTupleListDemo = [
    ('Peter', 'Lowstreet 4'),
    ('Amy', 'Apple st 652'),
    ('Hannah', 'Mountain 21'),
    ('Michael', 'Valley 345'),
    ('Sandy', 'Ocean blvd 2'),
    ('Betty', 'Green Grass 1'),
    ('Richard', 'Sky st 331'),
    ('Susan', 'One way 98'),
    ('Vicky', 'Yellow Garden 2'),
    ('Ben', 'Park Lane 38'),
    ('William', 'Central st 954'),
    ('Chuck', 'Main Road 989'),
    ('Viola', 'Sideway 1633')
]
createTableSpecified(getDB(), "customers", ["id INT AUTO_INCREMENT PRIMARY KEY",
                                             "name VARCHAR(255)",
                                             "address VARCHAR(255)"])
insertRows(getDB(), "customers", keyTupleDemo, valueTupleListDemo)
