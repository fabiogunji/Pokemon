
volumes:
  - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql


/*
CREATE TABLE IF NOT EXISTS stgpokemon (id SERIAL PRIMARY KEY,nome VARCHAR(100) NOT NULL,geral TEXT,data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS pokemon (id SERIAL PRIMARY KEY,nome VARCHAR(100) UNIQUE NOT NULL,geracao VARCHAR(50),hp INT,ataque INT,defesa INT,velocidade
*/ 