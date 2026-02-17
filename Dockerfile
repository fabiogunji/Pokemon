FROM python:3.11-slim

WORKDIR /app

# Instala as dependências
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Copia tudo
COPY . .

# Define o caminho do Python
ENV PYTHONPATH=/app/api

# Comando para rodar
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]