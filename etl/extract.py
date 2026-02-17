import requests
from etl.transform import transformarDados
import logging

logging.basicConfig( filename="main.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")


listaDadosGerais = []

def buscarPokemonNome(nome):
    try:
        logging.info(f"Busca de Pokemon na API por Nome: {nome}")    
    
        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"    
        resGeral = requests.get(url)            
        data = resGeral.json()
        
        print('Vai transformação')
            
        # Transforma valores
        transformarDados(nome,resGeral)
        
        print('FIM transformação')
        
    except Exception as e: 
        # tratamento do erro         
        logging.error(f"Erro ao buscar os dados na API do Pokemon {nome}: {e}")
        logging.exception(f"Erro ao buscar os dados na API do Pokemon {nome}: {e}")
        
    return resGeral


def buscar_imagem_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        # A URL da imagem fica dentro de 'sprites'
        url_imagem = dados['sprites']['front_default']
        return url_imagem
    else:
        return "Pokémon não encontrado!"

    
    '''
    listaDadosGerais.append(data)
    
    # Extrair os tipos 
    tipos = [t['type']['name'] for t in data['types']]   
    
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    
    
    # Depois consulta o endpoint species 
    url_species = f"https://pokeapi.co/api/v2/pokemon-species/{nome}" 
    data_species = requests.get(url_species).json() 
    
    # O campo 'generation' traz a URL e o nome da geração     
    generation = data_species['generation']['name']
    
    
    lista3 = [*tipos, *stats,*data_species]
    return lista3
    '''
    #return resGeral
 