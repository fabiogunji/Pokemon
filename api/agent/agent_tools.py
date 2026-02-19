import os
import logging 
from agents import tool


from etl.db_connection import get_connection # Usa sua conexão já criada
 
logging.basicConfig( filename="agent.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")

@tool
def buscar_pokemon_no_banco(nome: str) -> dict:
    """
    Busca os status e informações de um Pokémon específico no banco de dados local.
    """
    
    logging.info(f"Agente de busca de Pokemon no banco a API por Nome: {nome}")    
    
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

        logging.info(f"Final do a gente de busca de Pokemon no banco a API por Nome: {nome}") 
        
        return dict(zip(cols, row))
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cur.close()
        conn.close()

@tool
def listar_por_tipo(tipo: str) -> dict:
    """
    Lista todos os Pokémons de um determinado tipo (tipo_1 ou tipo_2).
    """
    logging.info(f"Lista Pokemon por tipo") 
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT nome FROM pokemon WHERE tipo_1 = %s OR tipo_2 = %s"
        cur.execute(query, (tipo.lower(), tipo.lower()))

        logging.info(f"Final da lista Pokemon por tipo") 

        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        return []
    finally:
        cur.close()
        conn.close()
        
@tool
def top_n_por_stat(stat: str, n: int = 5) -> dict:
    """
    Retorna o ranking dos top N Pokémons baseando-se em uma estatística específica.
    Estatísticas válidas: hp, ataque, defesa, velocidade.
    """
    logging.info(f"Lista Pokemon por estatisticas") 
    valid_stats = ['hp', 'ataque', 'defesa', 'velocidade']
    if stat.lower() not in valid_stats:
        return {"erro": f"Estatística inválida. Use uma destas: {', '.join(valid_stats)}"}

    try:
        conn = get_connection()
        cur = conn.cursor()
        # Usamos f-string apenas para o nome da coluna (stat), que validamos acima
        query = f"SELECT nome, {stat.lower()} FROM pokemon ORDER BY {stat.lower()} DESC LIMIT %s"
        cur.execute(query, (n,))
        rows = cur.fetchall()

        logging.info(f"Final da lista Pokemon por estatisticas") 

        return [{"nome": row[0], stat.lower(): row[1]} for row in rows]
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cur.close()
        conn.close()

@tool
def comparar_pokemons(pokemon_a: str, pokemon_b: str) -> dict:
    """
    Busca e compara as estatísticas de dois Pokémons diferentes.
    """
    
    logging.info(f"Compara Pokemons") 
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT nome, hp, ataque, defesa, velocidade, tipo_1, tipo_2 FROM pokemon WHERE nome IN (%s, %s)"
        cur.execute(query, (pokemon_a.lower(), pokemon_b.lower()))
        rows = cur.fetchall()
        
        if not rows:
            return {"erro": "Nenhum dos Pokémons foi encontrado para comparação."}
        
        cols = [desc[0] for desc in cur.description]
        resultado = [dict(zip(cols, row)) for row in rows]

        logging.info(f"Final do Compara Pokemons") 

        return {"comparacao": resultado}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cur.close()
        conn.close()