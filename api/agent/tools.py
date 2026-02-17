from openai_agents import Agent, Runner
from agent_tools import buscar_pokemon_db, listar_por_tipo
import os

# Define o Agente
poke_agent = Agent(
    name="PokeAnalyst",
    instructions="Você é um especialista em Pokémon. Use as ferramentas para consultar dados no banco de dados local antes de responder.",
    functions=[buscar_pokemon_db, listar_por_tipo],
    model="gpt-4o"
)

def ask_agent(pergunta: str):
    # Executa a conversa
    result = Runner.run(poke_agent, pergunta)
    print(f"IA: {result.final_response}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ask_agent(sys.argv[1])