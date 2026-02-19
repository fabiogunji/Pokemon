# Variáveis para evitar repetição
COMPOSE = docker compose
AGENT_RUN = $(COMPOSE) run --rm agent
PYTHON_EXEC = python api/agent/main_agent.py

.PHONY: setup up down etl ask logs clean test-db

# 1. Instalação: Build das imagens Docker
setup:
	$(COMPOSE) build

# 2. Infraestrutura: Sobe o banco de dados e a API em background
up:
	$(COMPOSE) up -d db api
	@echo "Aguardando o banco iniciar..."
	sleep 5

# 3. ETL: Executa o pipeline de dados (Extração, Transformação e Carga)
# Ajuste o caminho se o seu arquivo de entrada do ETL for diferente
etl:
	$(COMPOSE) run --rm api python etl/main.py

# 4. Agente: Faz uma pergunta para a IA
# Uso: make ask QUERY="Quais os tipos do Pikachu?"
ask:
	$(AGENT_RUN) python api/agent/main_agent.py "$(QUERY)"

# 5. Logs: Monitora os logs em tempo real
logs:
	$(COMPOSE) logs -f agent

# 6. Limpeza: Derruba os containers e limpa volumes órfãos
clean:
	$(COMPOSE) down --remove-orphans

# 7. Diagnóstico: Verifica se o agente consegue ver a chave da OpenAI e o banco
test-env:
	$(AGENT_RUN) /bin/sh -c "echo Chave: \$$OPENAI_API_KEY && python api/agent/teste_conexao.py"