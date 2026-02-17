
import psycopg2

import os

def get_connection():
    # O os.getenv busca a variável definida no Docker, 
    # se não achar (rodando local), usa o padrão depois da vírgula
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "pokedb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASS", "admin"),
        host=os.getenv("DB_HOST", "db"), # Nome do serviço no compose
        port=os.getenv("DB_PORT", "5432")
    )
    return conn



#LOCAL
'''
def get_connection():
    conn = psycopg2.connect(
        dbname="PokeDb",
        user="postgres",
        password="1010",
        host="localhost",
        port="5433"
    )
    
    return conn
'''

