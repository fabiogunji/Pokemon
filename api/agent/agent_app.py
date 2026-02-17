import os
import logging 


from etl.db_connection import get_connection # Usa sua conexão já criada
 
logging.basicConfig( filename="agent.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")


def buscar_pokemon_db(nome: str) -> dict:
    """
    Busca detalhes de um Pokémon específico no banco de dados local.
    """
    try:        
        conn = get_connection()
        cur = conn.cursor()
        # Busca na tabela que você criou
        cur.execute("SELECT * FROM pokemon WHERE nome = %s", (nome.lower(),))
        row = cur.fetchone()
        
        if not row:
            return {"erro": "Pokémon não encontrado no banco local."}
        
        # Mapeia colunas (ajuste conforme seu script SQL)
        cols = [desc[0] for desc in cur.description]
        
        return dict(zip(cols, row))
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cur.close()
        conn.close()

def listar_por_tipo(tipo: str) -> list:
    """
    Lista todos os Pokémons de um determinado tipo (tipo_1 ou tipo_2).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT nome FROM pokemon WHERE tipo_1 = %s OR tipo_2 = %s"
        cur.execute(query, (tipo.lower(), tipo.lower()))
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()