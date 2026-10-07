CREATE DATABASE ARABIA;
use ARABIA;
CREATE TABLE usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    endereco VARCHAR(255),
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE funcionario (
    idFuncionario INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL UNIQUE,
    cargo VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    dataAdmissao DATE NOT NULL,
    CONSTRAINT fk_func_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

CREATE TABLE cliente (
    idCliente INT AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL UNIQUE, 
    dataCadastro DATE NOT NULL,
    CONSTRAINT fk_cliente_usuario FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

CREATE TABLE produto (
    idProduto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    quantidade INT NOT NULL 
);

CREATE TABLE venda (
    idVenda INT AUTO_INCREMENT PRIMARY KEY,
    idFuncionario INT NOT NULL,
    idCliente INT NOT NULL,
    dataVenda DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    formaPagamento VARCHAR(50),
    CONSTRAINT fk_venda_func FOREIGN KEY (idFuncionario) REFERENCES funcionario(idFuncionario),
    CONSTRAINT fk_venda_cliente FOREIGN KEY (idCliente) REFERENCES cliente(idCliente)
);

CREATE TABLE pedido (
    idPedido INT AUTO_INCREMENT PRIMARY KEY,
    idVenda INT NOT NULL,
    idProduto INT NOT NULL,
    quantidade INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_pedido_venda FOREIGN KEY (idVenda) REFERENCES venda(idVenda) ON DELETE CASCADE,
    CONSTRAINT fk_pedido_produto FOREIGN KEY (idProduto) REFERENCES produto(idProduto)
);