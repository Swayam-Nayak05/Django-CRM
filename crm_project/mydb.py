import mysql.connector

db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="***********",
)

cursorobject = db.cursor()

cursorobject.execute("CREATE DATABASE crm_db")
