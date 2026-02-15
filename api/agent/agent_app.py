import requests

listaDadosGerais = []

nome = input("Digite o nome do pokemon para pesquisa: ")    

def listaDadosPokemonsAgente(nomePoke):    
    url = f"https://pokeapi.co/api/v2/pokemon/{nomePoke}"    
    resGeral = requests.get(url)    
    listaDadosGerais.append(resGeral.json())
    


    
listaDadosPokemonsAgente(nome)

#print(type(listaDadosGerais))
#dicio = dict(enumerate(listaDadosGerais))

#print(type(dicio))
print(listaDadosGerais)
