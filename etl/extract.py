import requests
from etl.transform import transformarDados
from etl.load import peqsuisa_pokemon_banco
import logging

logging.basicConfig( filename="main.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")


listaDadosGerais = []

def buscarPokemonNome(nome):
    try:
        logging.info(f"Inicio da busca de Pokemon na API por Nome: {nome}")    
    
        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"    
        resGeral = requests.get(url)            
        data = resGeral.json()
        
        # Transforma valores
        transformarDados(nome,resGeral)      

        logging.info(f"Final da busca de Pokemon na API por Nome: {nome}")    

        
    except Exception as e: 
        # tratamento do erro         
        logging.error(f"Erro ao buscar os dados na API do Pokemon {nome}: {e}")
        logging.exception(f"Erro ao buscar os dados na API do Pokemon {nome}: {e}")
        
    return resGeral


def buscar_imagem_pokemon(nome):
    logging.info(f"Inicio da busca de image do Pokemon na API por Nome: {nome}")    

    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        # A URL da imagem fica dentro de 'sprites'
        url_imagem = dados['sprites']['front_default']

        logging.info(f"Final da busca de image do Pokemon na API por Nome: {nome}")    
        return url_imagem
    else:
        logging.info(f"Inicio da busca de image do Pokemon na API por Nome: {nome}")    
        return "Pokémon não encontrado!"

    
def peqsuisa_pokemon(nome: str):
    try:        
        logging.info(f"Inicio da pesquisa de Pokemon: {nome}")    
        dadosPokemom =  peqsuisa_pokemon_banco(str)          
       
        if dadosPokemom:            
            return dadosPokemom

        logging.info(f"Final da pesquisa de Pokemon: {nome}")    

        return None
    
    except Exception as e:
        logging.error(f"Erro ao buscar no banco: {e}")
        return None
    
   