import requests
import sys
import os
import logging
from etl.extract import buscarPokemonNome,peqsuisa_pokemon
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import pandas as pd


logging.basicConfig(filename="main.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                    encoding="utf-8")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
        <head>
            <title>Busca de Pokemon</title>
            <style>
                body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #ffcc00, #ff6699); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); text-align: center; }
                input[type="text"] { padding: 10px; width: 80%; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 15px; }
                input[type="submit"] { background-color: #ff6699; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Digite o nome do Pokemon</h2>               
                <form action="/pokemon" method="post">
                    <input type="text" name="nome" placeholder="Digite o nome do Pokémon" required>
                    <input type="submit" value="Pesquisar">
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/pokemon", response_class=HTMLResponse)
async def get_pokemon(nome: str = Form(...)):
    try:
        dados = buscarPokemonNome(nome.lower())
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: linear-gradient(135deg, #ffcc00, #ff6699); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                    .container {{ background-color: white; padding: 30px; border-radius: 10px; text-align: center; }}
                    pre {{ text-align: left; background: #f9f9f9; padding: 15px; border-radius: 5px; overflow-x: auto; max-width: 500px; }}
                </style>            
            </head>
            <body>
                <div class="container">
                    <h2>Pokemon pesquisado: {nome}</h2>
                    <pre>{dados}</pre>                
                    <p><a href="/">Voltar</a></p>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html)
    except Exception as e:
        logging.error(f"Erro ao buscar pokemon: {e}")
        return HTMLResponse(content="<h2>Erro ao processar busca. Verifique o log.</h2>")
    
    

@app.post("/pesquisa", response_class=HTMLResponse)
async def pesquisar_pokemon(nome: str = Form(...)):
    # 1. Busca no banco de dados (tabela final)
    pokemon_dados = peqsuisa_pokemon(nome.lower())
    try:
        # Busca os dados no banco (certifique-se de que a função retorna um dicionário)
        pokemon = peqsuisa_pokemon(nome.lower())
        
        if not pokemon:
            # Conteúdo de erro com link para voltar
            conteudo = f"""
                <p style='color: #d9534f; font-weight: bold;'>O Pokémon '{nome}' não foi encontrado.</p>
                <a href="/" style="text-decoration: none; color: #ff6699; font-weight: bold;">← Voltar para a pesquisa</a>
            """
            return montar_pagina(conteudo_extra=conteudo)
        
        # Conteúdo de sucesso com os dados e link para voltar
        card_html = f"""
            <div style="margin-top: 20px; padding: 15px; border: 1px solid #eee; border-radius: 8px; background-color: #fafafa; text-align: left;">
                <h3 style="color: #ff6699; text-align: center;">{pokemon['nome'].upper()}</h3>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p><strong>Tipo:</strong> {pokemon['tipo_1']} {f'/ {pokemon["tipo_2"]}' if pokemon['tipo_2'] else ''}</p>
                <p><strong>HP:</strong> {pokemon['hp']}</p>
                <p><strong>Ataque:</strong> {pokemon['ataque']}</p>
                <p><strong>Defesa:</strong> {pokemon['defesa']}</p>
                <p><strong>Velocidade:</strong> {pokemon['velocidade']}</p>
            </div>
            <br>
            <a href="/" style="text-decoration: none; color: #ff6699; font-weight: bold;">← Pesquisar outro Pokémon</a>
        """
        return montar_pagina(conteudo_extra=card_html)
        
    except Exception as e:
        erro_msg = f"<p style='color: red;'>Erro: {str(e)}</p><a href='/'>Voltar</a>"
        return montar_pagina(conteudo_extra=erro_msg)

    
async def montar_pagina(conteudo_extra=""):
    return f"""
        <html>
        <head>
            <title>Busca de Pokemon</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(135deg, #ffcc00, #ff6699); 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    height: 100vh; 
                    margin: 0; 
                }}
                .container {{ 
                    background-color: white; 
                    padding: 30px; 
                    border-radius: 10px; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                    text-align: center; 
                    width: 350px; 
                }}
                input[type="text"] {{ padding: 10px; width: 80%; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 15px; }}
                input[type="submit"] {{ background-color: #ff6699; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }}
                input[type="submit"]:hover {{ background-color: #e65587; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Pesquisa Pokédex</h2>
                <form action="/pokemon" method="post">
                    <input type="text" name="nome" placeholder="Digite o nome..." required>
                    <input type="submit" value="Pesquisar">
                </form>
                {conteudo_extra}
            </div>
        </body>
        </html>
        """