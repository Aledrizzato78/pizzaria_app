import sqlite3
import os

# Caminho do arquivo SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'pizzaria.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')


def get_connection():
    """
    Retorna uma conexão com o banco SQLite.
    Cria o arquivo e inicializa o schema se não existir.
    """
    need_init = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    if need_init:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    return conn