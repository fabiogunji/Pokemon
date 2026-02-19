from etl.db_connection import get_connection
import logging 
 
logging.basicConfig( filename="load.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")
 
def pesquisaStgPokemon(nome):        
    logging.info(f"Pesquisa de Pokemons na tabela Stage: {nome}")

    idStgPokemon = 0

    conn = get_connection()
    print('ini cursor')
    cur = conn.cursor()    
        
    cur.execute("""
        SELECT  max("Id") FROM public."StgPokemon" WHERE "Nome" = %s
    """, (nome)
    )
    
    resultados = cur.fetchall() 
    for linha in resultados:
         idStgPokemon = linha["IdPokemon_seq"]

        
    logging.info(f"Final da pesquisa de Pokemons na tabela Stage: {nome}")

    return idStgPokemon
 

def carregarDadosStgPokemons(nome, lista):        
    try:
        logging.info(f"Inserção de Pokemons na tabela Stage: {nome}")        
        conn = get_connection()
        print('ini cursor')
        cur = conn.cursor()    
          
        cur.execute("""
            INSERT INTO public.stgpokemon(nome, geral) VALUES (%s, %s)
        """, (nome, lista)        
        )          
        
        conn.commit()                
        logging.info(f"Status inclusão do Pokemon: {nome} , status {cur.rowcount}")
        
    except Exception as e: # tratamento do erro         
        logging.error(f"Erro ao inserir dados dp Pokenmon na tabela Stage {nome}: {e}")
        logging.exception(f"Erro ao inserir dados dp Pokenmon na tabela Stage {nome}: {e}")
    finally: 
        cur.close() 
        conn.close()

def carregarDadosPokemons(p):
    logging.info(f"Inserção de Pokemons na tabela: {p['nome']}")     
    conn = get_connection() # Usando seu db_connection.py corrigido
    cur = conn.cursor()
    try:
        sql = """
            INSERT INTO pokemon (nome, geracao, hp, ataque, defesa, velocidade, tipo_1, tipo_2, altura, peso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nome) DO UPDATE SET
                geracao = EXCLUDED.geracao,
                hp = EXCLUDED.hp,
                ataque = EXCLUDED.ataque,
                defesa = EXCLUDED.defesa,
                velocidade = EXCLUDED.velocidade,
                tipo_1 = EXCLUDED.tipo_1,
                tipo_2 = EXCLUDED.tipo_2,
                altura = EXCLUDED.altura,
                peso = EXCLUDED.peso;
        """
        cur.execute(sql, (
            p['nome'], p['geracao'], p['hp'], p['ataque'], 
            p['defesa'], p['velocidade'], p['tipo_1'], 
            p['tipo_2'], p['altura'], p['peso']
        ))

        logging.info(f"Inserção de Pokemons na tabela: {p['nome']}")     

        conn.commit()

    except Exception as e:
        logging.error(f"Erro ao inserir dados dp Pokenmon na tabela {p['nome']}: {e}")
        logging.exception(f"Erro ao inserir dados dp Pokenmon na tabela {p['nome']}: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def peqsuisa_pokemon_banco(nome):
    try:

        logging.info(f"Busca de Pokemons na tabela: {nome}")     

        conn = get_connection() # Usa sua função de conexão existente
        cur = conn.cursor()
        
        # Busca na tabela final pelos dados estruturados
        query = "SELECT nome, geracao, hp, ataque, defesa, velocidade, tipo_1, tipo_2, altura, peso FROM pokemon WHERE nome = %s"
        cur.execute(query, (nome.lower(),))
        row = cur.fetchone()
        
        if row:
            # Transforma o resultado em um dicionário para facilitar o uso no HTML
            cols = [desc[0] for desc in cur.description]           
            return dict(zip(cols, row))

        logging.info(f"Final da Busca de Pokemons na tabela: {nome}")

        return None
    
    except Exception as e:
        logging.error(f"Erro ao buscar no banco: {e}")
        return None
    finally:
        cur.close()
        conn.close()
    
 