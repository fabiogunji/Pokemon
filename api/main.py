import requests
import pandas as pd
from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse
from etl.extract import buscarPokemonNome # Certifique-se que o caminho está correto
import logging

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
        dados = buscarPokemonNome(nome)
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