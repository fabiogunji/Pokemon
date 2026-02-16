FROM python:3.11-slim

# Define a pasta onde as coisas vão ficar dentro do Docker
WORKDIR /app

# Copia o arquivo de texto para dentro do Docker
COPY req.txt .

# Instala as bibliotecas corretamente usando o -r
RUN pip install --no-cache-dir -r req.txt

# Copia todo o seu projeto (pastas api, etl, etc) para o Docker
COPY . .

# Comando para iniciar sua API
CMD ["uvicorn", "api.teste2:app", "--host", "0.0.0.0", "--port", "8000"]