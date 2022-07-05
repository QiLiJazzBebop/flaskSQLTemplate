import mysql.connector
from datetime import date
from pathlib import Path
import traceback
import sys


## mysql booklet
## https://dev.mysql.com/doc/refman/8.0/en/data-types.html
## https://www.w3schools.com/sql/func_mysql_cast.asp

def get_project_root() -> Path:
    """
    Get the root path of project
    :return: None
    :rtype: None
    """
    return Path(__file__).parent.parent.__str__()


def exceptionLog(operation=""):
    """
    log error of sql operation to log file
    :param operation: sql Operation
    :type operation: String
    :param exception: the exception occur
    :type exception: Exception
    :return: None
    :rtype: None
    """
    f = open(get_project_root() + "/log/exception_" + date.today().__str__(), "a+")
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)
    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    f.write("Exception type : %s " % ex_type.__name__ + "\n")
    f.write("Exception message : %s" % ex_value + "\n")
    f.write("Stack trace : %s" % stack_trace + "\n")
    f.write("sql operation : %s" % operation + "\n")
    f.write("\n")

    f.close


def getDBServer(host="localhost", user="root", password="?Aa13552676625"):
    """
    get the database server
    :param host: the host name
    :type host: String
    :param user: the username
    :type user: String
    :param password: the passwd for this user
    :type password: String
    :param database: the database you want to log in
    :type database: String
    :return: db connector
    :rtype: Union[CMySQLConnection, MySQLConnection]
    """
    try:
        db = mysql.connector.connect(host=host, user=user, password=password)
    except:
        print("Fail to connect")
        exceptionLog("fail to connect to sql")
        sys.exit(0)
    return db


def getDB(host="localhost", user="root", password="?Aa13552676625", database="envTestMark2"):
    """
    get the database be operated
    :param host: the host name
    :type host: String
    :param user: the username
    :type user: String
    :param password: the passwd for this user
    :type password: String
    :param database: the database you want to log in
    :type database: String
    :return: db connector
    :rtype: Union[CMySQLConnection, MySQLConnection]
    """
    try:
        db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    except:
        print("Fail to connect")
        exceptionLog("fail to connect to sql")
        sys.exit(0)
    return db


def createDatabase(db, dataBaseName):
    """
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    Create a database by given name if it exists.
    :param dataBaseName: database name
    :type dataBaseName: String
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    sqlQuery = "CREATE DATABASE IF NOT EXISTS " + dataBaseName
    try:
        # create database if it not exists
        cursor.execute(sqlQuery)
        db.commit()
    except Exception as e:
        print("Fail to create database")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        cursor.close()
        db.close()


def dropDatabase(db, dataBaseName):
    """
    Delete a database by given name if it exists, Double check in case.
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param dataBaseName: database name
    :type dataBaseName: String
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    # double authentication
    print("double check if you want to delete the database: ", dataBaseName, "YES/NO")
    check = input()
    sqlQuery = "DROP DATABASE IF EXISTS " + dataBaseName
    # delete database if it not exists
    try:
        if check.__eq__("YES"):
            cursor.execute("DROP DATABASE IF EXISTS " + dataBaseName)
    except Exception as e:
        print("fail to drop the database")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        cursor.close()
        db.close()


def createTableSpecified(db, tableName, elementList):
    """
    Create a table by given table name, where each element's name and type should be specified
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param tableName: The name of table
    :type tableName: String
    :param elementList: Specify the names of the columns of the table, [column1 datatype, column2 datatype, ...]
    :type elementList: List of string
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    # iteratively read element to insert to the query
    sqlQuery = "CREATE TABLE IF NOT EXISTS " + tableName + " ("
    for element in elementList:
        sqlQuery += element
        sqlQuery += ", "
    sqlQuery = sqlQuery[:-2] + ")"
    try:
        cursor.execute(sqlQuery)
        db.commit()
    except:
        print("fail to create the table")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        cursor.close()
        db.close()


def dropTable(db, tableName):
    """
    Drop a table by given table name when it exists
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param tableName: The name of table
    :type tableName: String
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    # drop table only it exists
    sqlQuery = "DROP TABLE IF EXISTS " + tableName
    try:
        cursor.execute("DROP TABLE IF EXISTS " + tableName)
        db.commit()
    except:
        print("fail to drop the table")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        cursor.close()
        db.close()


def insertRows(db, tableName, keyTuple: tuple, valueTupleList: list):
    """
    Insert multi rows to a given table
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param tableName: target table name
    :type tableName: String
    :param keyTuple: The tuple consist of key names
    :type keyTuple: Tuple
    :param valueTupleList: The list of value need to be inserted
    :type valueTupleList: List of Tuple
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    sqlQuery = "INSERT INTO " + tableName + " (" + ', '.join(keyTuple) + ") VALUES (" + ", ".join(
        tuple(["%s"] * len(keyTuple))) + ")"
    try:
        cursor.executemany(sqlQuery, valueTupleList)
        db.commit()
    except:
        print("fail to insert the rows")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        cursor.close()
        db.close()

## example
## sql: UPDATE employees SET lastname = 'Hill',email = 'mary.hill@classicmodelcars.com WHERE employeeNumber = 1056;


def dbUpdate(db, sqlQuery):
    """
    Given a query, execute the update operation
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param sqlQuery: the update query
    :type sqlQuery: String
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    try:
        cursor.execute(sqlQuery)
        db.commit()
    except:
        print("fail to update the rows")
        exceptionLog(sqlQuery)
        db.rollback()
    finally:
        print(cursor.rowcount, "records(s) deleted")
        cursor.close()
        db.close()


## example
## sql: SELECT name, address FROM customers
## sql: SELECT * FROM customers WHERE address ='Park Lane 38'
## sql: SELECT * FROM customers ORDER BY name DESC
## sql: SELECT * FROM customers LIMIT 5 OFFSET 2

def dbSelect(db, sql):
    """
    Select rows as return, Enable sql command as input, and return result as a list comprise of tuples
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param sql: sql command
    :type sql: String
    :return: list of tuples
    :rtype: List
    """
    cursor = db.cursor()
    res = []
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
    except:
        db.rollback()
    finally:
        print(cursor.rowcount, "record(s) selected")
        cursor.close()
        db.close()

        return res


## example
## sql: DELETE FROM customers WHERE address = 'Mountain 21'

def dbDelete(db, sql):
    """
    Delete rows, Enable sql command as input
    :param db: database to run query
    :type db: Union[CMySQLConnection, MySQLConnection]
    :param sql: sql command
    :type sql: String
    :return: None
    :rtype: None
    """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    finally:
        print(cursor.rowcount, "records(s) deleted")
        cursor.close()
        db.close()
