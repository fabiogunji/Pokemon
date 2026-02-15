import requests
import pandas as pd
from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse
from etl.extract import buscarPokemonNome
import logging

logging.basicConfig( filename="main.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",encoding="utf-8")

app = FastAPI()

#listaNomes = []
#listaHabilidades = []
#listaTipos = [] 
#listaMovimentos = []
#listaDadosGerais = []

try:
    # Monta tela para pesquisa de nome de Pokemons
    @app.get("/", response_class=HTMLResponse)
    def form():
        return """
        <html>
            <head>
                <title>Busca de Pokémon</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #ffcc00, #ff6699);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .container {
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        text-align: center;
                    }
                    h2 {
                        color: #333;
                    }
                    input[type="text"] {
                        padding: 10px;
                        width: 80%;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        margin-bottom: 15px;
                    }
                    input[type="submit"] {
                        background-color: #ff6699;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-weight: bold;
                    }
                    input[type="submit"]:hover {
                        background-color: #ff3366;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Digite o nome do Pokémon</h2>				
                    <form action="/pokemon" method="post" onsubmit="this.querySelector('input[type=submit]').disabled=true;">
                        <input type="text" name="nome" placeholder="Digite o nome do Pokémon">
                        <input type="submit" value="Pesquisar">
                    </form>
                </div>
            </body>
        </html>
        """


    @app.post("/pokemon", response_class=HTMLResponse)
    def get_pokemon(nome: str = Form(...)):
        dados = buscarPokemonNome(nome)
        
        # exemplo simples de renderização
        html = f"""
        <html>
            <head>
                <title>Resultado da inclusão</title>
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
                            }}
                        h2 {{
                            color: #333;
                        }}
                        pre {{
                            text-align: left;
                            background: #f9f9f9;
                            padding: 15px;
                            border-radius: 5px;
                            overflow-x: auto;
                        }}
                    </style>            
            </head>
            <body>
                <h2>Pokémon inserido: {nome}</h2>
                <pre>{dados}</pre>
                <br>
                <br>
                <a href="/" class="btn">Voltar</a>
            </body>
        </html>
        """
        return HTMLResponse(content=html)

except Exception as e: 
        # tratamento do erro         
        logging.error(f"Erro na página principal: {e}")
        logging.exception(f"Erro na página principal: {e}")
        

if __name__ == '__main__':
    form()
    
'''

@app.post("/pokemon")
def get_pokemon(nome: str = Form(...)): 
    return dict(enumerate(buscarPokemonNome(nome)))




    #url = f"https://pokeapi.co/api/v2/pokemon/{nome}"    
    #resGeral = requests.get(url)    
    #listaDadosGerais.append(resGeral.json())
    #return dict(enumerate(listaDadosGerais))     


def habilidades(pokemons):
    print('Habilidades')
    for i in pokemons['abilities']:   
        listaHabilidades.append(i['ability']['name'])
    
    print(listaHabilidades) 
        #print('*-'+i['ability']['name'])
        

def movimentos(pokemons):
    print('Movimentos')
    for i in pokemons['moves']:    
        listaMovimentos.append(i['move']['name'])    
    print(listaMovimentos)
        # print('%'+i['move']['name'])        

### Busca na API a lista com os nome de todos os pokemons
def nome(pokemons):
    print('Nomes')
    for i in pokemons['results']:              
        listaNomes.append(i['name'])        
        #listaDadosPokemons(i['name'])      
    print(listaNomes)
    #print(listaDadosGerais)    
    #print(listaNomes)  
        #print('#'+i['name'])    
       
def listaDadosPokemonsAgente(nome):
    resGeral = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}")    
    listaDadosGerais.append(resGeral)
    
        
def tipos(pokemons):
    print('types')
    for i in pokemons['types']:    
        listaTipos.append(i['type']['name'])
    print(listaTipos)
        # print('@'+i['type']['name'])       
'''    

    
    #nome = input("Digite o nome do pokemon para pesquisa: ")
    
    #apiNome = "https://pokeapi.co/api/v2/pokemon?limit=1500&offset=0"
    
    #api = "https://pokeapi.co/api/v2/pokemon/pikachu"
    
    #resNome = requests.get(apiNome)    
    #resApi = requests.get(api)          
    
    #nome(resNome.json()) 
    #habilidades(resApi.json()) 
    #movimentos(resApi.json()) 
    #tipos(resApi.json()) 
    



