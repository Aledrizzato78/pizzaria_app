-- Criação das tabelas clientes e pedidos
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT UNIQUE NOT NULL,
    endereco TEXT,
    data_vencimento_locacao DATE
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    sabor TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    datahora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
);