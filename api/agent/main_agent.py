import os
import sys
import logging
import asyncio

from agents import Agent, Runner, Tool
from agent_tools import (
    buscar_pokemon_no_banco,
    listar_por_tipo,
    top_n_por_stat,
    comparar_pokemons
)

logging.basicConfig( filename="mainagent.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")

logging.info(f"Montando o prompt para a IA")  

try:
    tools = [
        Tool.from_function(buscar_pokemon_no_banco),
        Tool.from_function(listar_por_tipo),
        Tool.from_function(top_n_por_stat),
        Tool.from_function(comparar_pokemons),
]


    # Mapeamento para o Runner saber qual função Python executar
    exec_map = {
        "buscar_pokemon_no_banco": buscar_pokemon_no_banco,
        "listar_por_tipo": listar_por_tipo,
        "top_n_por_stat": top_n_por_stat,
        "comparar_pokemons": comparar_pokemons
    }
   
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
        tools=tools
    )     
except Exception as e:
    logging.error(f"Erro no agente {e}")
    logging.exception(f"Erro no agente {e}")



async def main():
    # Verifica se a chave subiu para o container
    key = os.getenv("OPENAI_API_KEY")
    if not key or not key.startswith("sk-"):
        logging.info("[ERRO]: OPENAI_API_KEY não detectada ou inválida dentro do container!")
        return

    if len(sys.argv) > 1:
        pergunta = " ".join(sys.argv[1:])
        logging.info(f"Lançando pergunta: {pergunta}")
        
        try:            
            # Execução do Runner
            result = await Runner.run(poke_agent, pergunta)
            
            # Se a resposta final estiver vazia, vasculhamos as mensagens
            if hasattr(result, 'final_response') and result.final_response:
                logging.info(f"\n[PokeAnalyst]: {result.final_response}")
            elif hasattr(result, 'messages'):
                for msg in reversed(result.messages):
                    if msg.role == "assistant" and msg.content:
                        logging.info(f"\n[PokeAnalyst]: {msg.content}")
                        return
                logging.info("\n[Aviso]: O Agente processou, mas não retornou texto. Verifique os logs do banco.")
                        
        except Exception as e:
            logging.error(f"\n[ERRO NA EXECUÇÃO]: {e}")
    
            
if __name__ == "__main__":
    asyncio.run(main())