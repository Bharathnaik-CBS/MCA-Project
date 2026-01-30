# utils/db_helpers.py
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bharath@1234",
        database="project_developers",
        connection_timeout=60
    )
