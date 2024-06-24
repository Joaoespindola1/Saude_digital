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

CREATE TABLE IF NOT EXISTS planos_saude (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_plano VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS corretores_planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    corretor_id INT NOT NULL,
    plano_id INT NOT NULL,
    FOREIGN KEY (corretor_id) REFERENCES corretores(id),
    FOREIGN KEY (plano_id) REFERENCES planos_saude(id),
    UNIQUE (corretor_id, plano_id)
);

INSERT INTO planos_saude (nome_plano, estado) VALUES 
('Unimed', 'Rio de Janeiro');

INSERT INTO clientes (nome, email, senha, cpf) VALUES
('Samuel', 'samuel@example.com', '123', '111.111.111-11'),
('Pipico', 'pipico@example.com', '123', '222.222.222-22');

INSERT INTO corretores (nome, email, senha, cpf, numero_registro) VALUES
('Yago', 'yago@example.com', '123', '333.333.333-33', 'CR12345'),
('Jão', 'jao@example.com', '123', '444.444.444-44', 'CR54321');


SELECT * FROM clientes;

SELECT * FROM corretores;