import requests
from etl.load import carregarDadosPokemons 
from etl.load import carregarDadosStgPokemons   
import logging 

logging.basicConfig( filename="transform.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")
   
def transformarDados(nome,resGeral):
    try:
        logging.info(f"Transformação de dados do Pokemon: {nome}")    
         
        print('INICIO transformação')
        data = resGeral.json()    
        
        # Extrair os tipos 
        tipos = [t['type']['name'] for t in data['types']]   
        
        # Estatísticas
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        
        # Depois consulta o endpoint species 
        url_species = f"https://pokeapi.co/api/v2/pokemon-species/{nome}" 
        data_species = requests.get(url_species).json() 
        
        # Geraççao
        generation = data_species['generation']['name']
    
        listaTransformada = [*tipos, *stats,*generation]
        
        listaTipo = [*tipos]
        listaEstatistica = [*stats]
        listaGeracao = [*data_species]
        
        print('FIM transformação')
        
        print('Vai StgPoke')
        
        # Armazena dados originais no banco
        carregarDadosStgPokemons(nome, listaTransformada)
        
        print('Fim StgPoke')
        
        print('INICIO Poke')
        
        carregarDadosPokemons(nome, listaTipo, listaEstatistica, listaGeracao)#listaTransformada)
            
        print('FIM LOAD')
        
    except Exception as e: # tratamento do erro         
        logging.error(f"Erro ao transformar dados do Pokemon {nome}: {e}")
        logging.exception(f"Erro ao transformar dados do Pokemon {nome}: {e}")
        
    return listaTransformada

