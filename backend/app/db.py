import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # Name of the database service in docker-compose.yml
        database="stockdb",
        user="postgresql",
        password="admin"
    )
    return conn
