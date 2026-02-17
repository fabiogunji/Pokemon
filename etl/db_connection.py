
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="PokeDb",
        user="postgres",
        password="1010",
        host="localhost",
        port="5433"
    )
    
    return conn
