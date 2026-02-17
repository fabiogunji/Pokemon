from etl.db_connection import get_connection
import logging 
 
logging.basicConfig( filename="load.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")
 
def pesquisaStgPokemon(nome):        
    logging.info(f"Inserção de Pokemons na tabela Stage: {nome}")

    idStgPokemon = 0

    conn = get_connection()
    print('ini cursor')
    cur = conn.cursor()    
    
    print('rodando insert')        
        
    cur.execute("""
        SELECT  max("Id") FROM public."StgPokemon" WHERE "Nome" = %s
    """, (nome)
    )
    
    resultados = cur.fetchall() 
    for linha in resultados:
         idStgPokemon = linha["IdPokemon_seq"]
    
    print(idStgPokemon)
    
    return idStgPokemon
 

def carregarDadosStgPokemons(nome, lista):        
    try:
        logging.info(f"Inserção de Pokemons na tabela Stage: {nome}")        
        conn = get_connection()
        print('ini cursor')
        cur = conn.cursor()    
          
        cur.execute("""
            INSERT INTO public.stgpokemon(nome, geral) VALUES (%s, %s)
        """, (nome, tuple(lista))        
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
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

'''
def carregarDadosPokemons(nome, listaTipo, listaEstatistica, listaGeracao):
    try:
        logging.info(f"Inserção de Pokemons na tabela: {nome}")
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO public.pokemon(nome, estatistica, geracao, tipo) VALUES (%s, %s, %s, %s)
        """, (nome,tuple(listaEstatistica), tuple(listaGeracao), tuple(listaTipo))
        )
        
        conn.commit()                
        logging.info(f"Status inclusão do Pokemon: {nome} , status {cur.rowcount}")
        
    except Exception as e: # tratamento do erro 
        logging.error(f"Erro ao inserir dados do Pokemon {nome}: {e}")
        logging.exception(f"Erro ao inserir dados do Pokemon {nome}: {e}")
    finally: 
        cur.close() 
        conn.close()
    
'''
    
    