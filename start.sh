#!/bin/bash

echo "=== Iniciando Orquestração do Projeto Pokémon ==="

# 1. Passo de Carga: Executa o ETL para garantir que o banco tenha dados
echo "[1/3] Extraindo dados da API..."
#python etl/extract.py

echo "[2/3] Transformando e carregando no Banco de Dados..."
#python etl/transform.py

# 2. Passo de Serviço: Inicia o main.py onde está o seu HTML
echo "[3/3] Iniciando Servidor Web (main.py)..."

# O comando abaixo procura o objeto 'app' dentro do arquivo 'api/main.py'
exec uvicorn api.main:app --host 0.0.0.0 --port 8000