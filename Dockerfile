# 1. Imagem base

FROM python:3.11-slim

# 2. Diretório de trabalho (Raiz da aplicação no container)
WORKDIR /app

# 3. Instala dependências do sistema para o banco de dados
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de dependências (usando o nome do seu print: req.txt)
COPY req.txt .

# 5. Instala as bibliotecas (incluindo openai-agents que deve estar no req.txt)
RUN pip install --no-cache-dir -r req.txt

# 6. Copia TODO o projeto para dentro do container
# Isso garante que main_agent.py e a pasta api/ existam lá dentro
COPY . .

# 7. Define o PYTHONPATH para que os scripts encontrem a pasta api
ENV PYTHONPATH=/app

# 8. Comando padrão para a API (o Compose pode sobrescrever para o Agent)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]