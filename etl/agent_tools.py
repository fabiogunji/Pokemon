import os
import logging
from etl.db_connection import get_connection

def buscar_pokemon_no_banco(nome: str):
    """Busca os status e informações de um Pokémon no banco de dados local."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pokemon WHERE nome = %s", (nome.lower(),))
        row = cur.fetchone()
        if row:
            cols = [desc[0] for desc in cur.description]
            return dict(zip(cols, row))
        return {"erro": "Pokémon não encontrado no banco."}
    finally:
        cur.close()
        conn.close()