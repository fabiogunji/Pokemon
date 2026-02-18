# Comandos de Orquestração

setup:
	docker-compose up -d db
	sleep 10
	docker-compose run --rm agent python scripts/create_tables.py

run-etl:
	docker-compose run --rm agent python etl/extract.py
	docker-compose run --rm agent python etl/transform.py

run-agent:
	docker-compose run --rm agent python api/agent/main_agent.py "Quais são os top 3 pokemons?"

full-pipeline: setup run-etl run-agent