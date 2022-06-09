import mysql.connector

db = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "",
    database = "picturefy" 
)

db.close()