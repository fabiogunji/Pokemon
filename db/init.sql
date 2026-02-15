

-- Criação de bando de dados

CREATE DATABASE "PokeDb"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "PokeDb"
    IS 'Base de dados de características de pokemons';

-- Criação do Schema

CREATE SCHEMA "Pokemons"
    AUTHORIZATION postgres;


CREATE TABLE stgpokemon (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(50),
    geral TEXT
);


CREATE TABLE pokemon (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(50),
	estatistica TEXT,
    geracao TEXT,
	tipo TEXT
);