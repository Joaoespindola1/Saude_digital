CREATE DATABASE IF NOT EXISTS saude_digital;

USE saude_digital;

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS corretores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    numero_registro VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO clientes (nome, email, senha, cpf) VALUES
('Samuel', 'samuel@example.com', '123', '111.111.111-11'),
('Pipico', 'pipico@example.com', '123', '222.222.222-22');

INSERT INTO corretores (nome, email, senha, cpf, numero_registro) VALUES
('Yago', 'yago@example.com', '123', '333.333.333-33', 'CR12345'),
('Jão', 'jao@example.com', '123', '444.444.444-44', 'CR54321');


SELECT * FROM clientes;

SELECT * FROM corretores;