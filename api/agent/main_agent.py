import os
import sys
import logging
import asyncio

from agents import Agent, Runner
#from openai import Agent, Runner
#from openai_agents import Agent, Runner
from agent_tools import buscar_pokemon_db, listar_por_tipo, top_n_por_stat, comparar_pokemons

logging.basicConfig( filename="mainagent.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")

logging.info(f"Montando o prompt para a IA")    


# 1. Configuração do Agente (Requisito: OpenAI Agents SDK)
poke_agent = Agent(
    name="PokeAnalyst",
    instructions = """
        Você é o 'PokeAnalyst', um Agente de IA especializado em análise de dados da franquia Pokémon. 
        Seu objetivo é fornecer informações precisas baseadas EXCLUSIVAMENTE no banco de dados local.

        ### REGRAS DE COMPORTAMENTO:
        1. **Prioridade de Dados:** Sempre que um usuário mencionar um Pokémon ou um Tipo, sua primeira ação deve ser chamar as funções 'buscar_pokemon_db' ou 'listar_por_tipo'.
        2. **Ausência de Dados:** Se a função retornar que o Pokémon não existe no banco, diga: "Infelizmente, o Pokémon [NOME] ainda não foi capturado pela nossa pipeline de ETL e não consta no banco de dados local."
        3. **Tom de Voz:** Seja profissional, técnico e prestativo. Use termos como 'Base Stats', 'Tipagem' e 'Geração'.
        4. **Unidades de Medida:** Ao informar altura, use metros (m). Ao informar peso, use quilogramas (kg).
        5. **Comparação:** Se o usuário pedir para comparar dois Pokémons, chame a ferramenta de busca para ambos e monte uma tabela técnica comparativa.

        ### RESTRIÇÕES:
        - Não invente estatísticas que não retornaram das funções.
        - Se o usuário perguntar algo fora do universo Pokémon, responda que seu conhecimento é restrito à Pokédex local.
""",
    tools=[buscar_pokemon_db, listar_por_tipo, top_n_por_stat, comparar_pokemons], 
    model="gpt-4o"
)

async def executar_pergunta(pergunta: str):
    """Executa a interação entre o usuário e a IA utilizando o Runner do SDK."""
    try:
        # O Runner gerencia automaticamente a chamada das tools (funções)
        result = Runner.run(poke_agent, pergunta)
        print(f"\n[IA PokeAnalyst]: {result.final_response}")
    except Exception as e:
        print(f"\n[Erro no Agente]: {e}")

if __name__ == "__main__":
    # Requisito: Modo simples de execução via CLI
    # Pega a pergunta passada pelo comando 'docker compose run'
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        asyncio.run(executar_pergunta(query))        
    else:
        print("Por favor, envie uma pergunta. Exemplo: docker compose run --rm agent 'Quem é o Pikachu?'")