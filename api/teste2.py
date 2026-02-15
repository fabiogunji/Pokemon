
import requests
from fastapi import FastAPI, Form 
from fastapi.responses import HTMLResponse

app = FastAPI()

listaDadosGerais = []


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <form action="/pokemon" method="post">
        <input type="text" name="nome" placeholder="Digite o nome do Pokémon">
        <input type="submit" value="Pesquisar">
    </form>
    """

@app.post("/pokemon")
def get_pokemon(nome: str = Form(...)):    
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"    
    resGeral = requests.get(url)    
    listaDadosGerais.append(resGeral.json())     
    
      
    return dict(enumerate(listaDadosGerais))



 