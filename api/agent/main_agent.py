import os
import sys

from openai_agents import Agent, Runner
from agent_tools import buscar_pokemon_db, listar_por_tipo

# 1. Configuração do Agente (Requisito: OpenAI Agents SDK)
poke_agent = Agent(
    name="PokeAnalyst",
    instructions="""
        Você é um especialista em Pokémon que analisa dados de um banco de dados local.
        Sempre que um usuário perguntar sobre um Pokémon ou tipos, use as ferramentas fornecidas.
        Se o dado não existir no banco, informe ao usuário.
        Responda de forma clara e técnica.
    """,
    functions=[buscar_pokemon_db, listar_por_tipo], # Requisito: implementar pelo menos 2 tools
    model="gpt-4o"
)

def executar_pergunta(pergunta: str):
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
        executar_pergunta(query)
    else:
        print("Por favor, envie uma pergunta. Exemplo: docker compose run --rm agent 'Quem é o Pikachu?'")