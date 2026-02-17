import requests
from etl.load import carregarDadosPokemons 
from etl.load import carregarDadosStgPokemons   
import logging 

logging.basicConfig( filename="transform.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")

import requests
import logging

def transformarDados(nome, resGeral):
    try:        
        logging.info(f"Iniciando transformação: {nome}")
        data = resGeral.json()
        
        # 1. Extração de Tipos (garante até 2 tipos)
        tipos = [t['type']['name'] for t in data['types']]
        tipo1 = tipos[0]
        tipo2 = tipos[1] if len(tipos) > 1 else None

        # 2. Extração de Estatísticas (Mapeia o nome ao valor real)
        stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        
        # 3. Busca de Espécie para pegar a Geração
        url_species = data['species']['url'] # Melhor usar a URL que vem no JSON original
        res_species = requests.get(url_species)
        data_species = res_species.json()
        geracao = data_species['generation']['name']

        # 4. Dados Complementares
        dados_pokemon = {
            "nome": nome,
            "geracao": geracao,
            "hp": stats.get('hp'),
            "ataque": stats.get('attack'),
            "defesa": stats.get('defense'),
            "velocidade": stats.get('speed'),
            "tipo_1": tipo1,
            "tipo_2": tipo2,
            "altura": data.get('height') / 10, # Converte para metros
            "peso": data.get('weight') / 10     # Converte para kg
        }

        # 5. Carga na Staging (Dados originais/brutos)
        # Convertemos para string para a coluna 'geral'
        carregarDadosStgPokemons(nome, str(dados_pokemon))

        # 6. Carga na Tabela Final (Passando o dicionário organizado)
        carregarDadosPokemons(dados_pokemon)
        
        logging.info(f"Fim da carga para {nome}")
        return dados_pokemon

    except Exception as e:
        logging.error(f"Erro na transformação de {nome}: {e}")
        logging.exception(f"Erro na transformação de {nome}: {e}")
        raise e

'''
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
'''
