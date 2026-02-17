

Comandos para executar no powershell - Docker

-- Criar imagem
docker build -t poke-imagem .

-- Para ambiente
docker-compose down -v

-- Start ambiente
docker-compose up -d

-- Remover container
docker rm poke-container

-- Verificar container publicados
docker ps

-- consulta de logs do container
docker logs poke-container-api


-- Consulta logs do container de banco de dados
docker logs poke-container-db

-- Acesso ao banco de dados remoto
docker exec -it poke-container-db psql -U admin -d pokedb