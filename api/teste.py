#pip install requests pandas matplotlib


import requests
import pandas as pd

def get_pokemon_data(limit=100):
    # Obtém uma lista de pokémons
    url = f"https://pokeapi.co{limit}"
    response = requests.get(url)
    results = response.json()['results']
    
    pokemon_list = []
    
    for pkmn in results:
        data = requests.get(pkmn['url']).json()
        
        # Estrutura os dados básicos
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        types = [t['type']['name'] for t in data['types']]
        
        pokemon_list.append({
            'name': data['name'],
            'id': data['id'],
            'types': types,
            'hp': stats.get('hp'),
            'attack': stats.get('attack'),
            'defense': stats.get('defense'),
            'special-attack': stats.get('special-attack'),
            'special-defense': stats.get('special-defense'),
            'speed': stats.get('speed'),
            'total_stats': sum(stats.values()),
            'generation': get_generation(data['species']['url'])
        })
    return pd.DataFrame(pokemon_list)

def get_generation(species_url):
    # Função auxiliar para pegar a geração da espécie
    species_data = requests.get(species_url).json()
    return species_data['generation']['name']

# --- Execução ---
# Pegando os primeiros 150 para exemplo
df_pokemon = get_pokemon_data(limit=150)
print(df_pokemon.head())



# 1. Filtrar por Tipo (ex: Fogo)
fire_types = df_pokemon[df_pokemon['types'].apply(lambda x: 'fire' in x)]
print("\nPokémons de Fogo:")
print(fire_types[['name', 'attack', 'special-attack']])

# 2. Distribuição de Stats (Média)
mean_stats = df_pokemon.groupby('types')[['hp', 'attack', 'defense', 'speed']].mean()
print("\nMédia de Stats por Tipo:")
print(mean_stats)


# Média de Total Stats por Geração
gen_comparison = df_pokemon.groupby('generation')['total_stats'].mean()
print("\nTotal Base Stats Médio por Geração:")
print(gen_comparison)


# Top 5 Pokémon com maior ataque
top_attack = df_pokemon.nlargest(5, 'attack')
print("\nTop 5 Pokémons por Ataque:")
print(top_attack[['name', 'attack']])

# Top 5 Pokémon com maior Total Stats
top_overall = df_pokemon.nlargest(5, 'total_stats')
print("\nTop 5 Pokémons mais fortes (Total):")
print(top_overall[['name', 'total_stats', 'types']])


'''
Resumo dos Endpoints Importantes da PokeAPI
Lista de Pokémons: https://pokeapi.co
Detalhes do Pokémon: https://pokeapi.co{id ou nome}/
Tipos: https://pokeapi.co/api/v2/type/{id ou nome}/
Gerações: https://pokeapi.co{id ou nome}/ 
Dica de Performance
Para análises que envolvem todos os +1000 pokémons, o requests pode ser lento. Considere usar aiohttp para chamadas assíncronas ou baixar um dataset pré-processado (como os do Kaggle, baseados na API) se a atualização em tempo real não for necessária. 
'''