"""
main.py: Ponto de entrada do aplicativo.
"""
import sys
from data.db import get_connection


def main():
    # Inicializa DB e exibe contagem de clientes
    conn = get_connection()
    c = conn.cursor()
    total = c.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
    print(f'Total de clientes cadastrados: {total}')
    conn.close()

    # TODO: chamar startup.py para validação de licença e GUI


if __name__ == '__main__':
    main()
