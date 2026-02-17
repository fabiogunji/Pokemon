import requests


def obter_status_pokemon(nome_pokemon):
    url = "https://pokeapi.co/api/v2/pokemon/pikachu/"
    
    try:
        response = requests.get(url)
        dados = response.json()
        
        # Criando um dicionário para facilitar a leitura
        status_dict = {}
        for s in dados['stats']:
            nome_stat = s['stat']['name']
            valor_stat = s['base_stat']
            status_dict[nome_stat] = valor_stat
            
        return status_dict
    except:
        return None

# Exemplo com o Machamp (conhecido pela força física)
stats = obter_status_pokemon("machamp")
if stats:
    print(f"Ataque Físico: {stats['attack']}")
    print(f"BST (Soma Total): {sum(stats.values())}")