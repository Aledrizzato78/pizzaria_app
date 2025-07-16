import datetime
import sqlite3
from data.db import get_connection
from license.generator import LicenseGenerator


class LicenseValidator:
    """
    Classe responsável por validar códigos de licença no aplicativo e atualizar
    o campo `data_vencimento_locacao` na tabela `clientes`.

    Exemplo de uso:
        validator = LicenseValidator(secret_key=b'minha_chave_secreta')
        exp_date = validator.validate_and_update(cliente_id=1, code=codigo)
    """

    def __init__(self, secret_key: bytes, mac_size: int=8):
        """
        Inicializa o validador de licença.

        :param secret_key: Mesma chave usada no LicenseGenerator.
        :param mac_size: Número de bytes do MAC (deve coincidir).
        """
        self.secret_key = secret_key
        self.mac_size = mac_size
        self.generator = LicenseGenerator(secret_key, mac_size)

    def validate_and_update(self, cliente_id: int, code: str) -> datetime.date:
        """
        Valida o código de licença e, se válido, atualiza a data de vencimento
        do cliente no banco de dados.

        :param cliente_id: ID do cliente a atualizar.
        :param code: Código de licença recebido via GUI.
        :return: Data de expiração extraída do código.
        :raises ValueError: Se o código for inválido ou corrompido.
        :raises sqlite3.Error: Se ocorrer erro na atualização do DB.
        """
        # Valida integridade e obtém data de expiração
        exp_date = self.generator.validate_code(code)

        # Atualiza banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE clientes
            SET data_vencimento_locacao = ?
            WHERE id = ?
            """,
            (exp_date.isoformat(), cliente_id)
        )
        conn.commit()
        conn.close()
        return exp_date

    def is_expired(self, cliente_id: int) -> bool:
        """
        Verifica se a licença do cliente expirou comparando a data no DB com hoje.

        :param cliente_id: ID do cliente a verificar.
        :return: True se expirou ou não encontrado; False se ainda válida.
        """
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute(
            "SELECT data_vencimento_locacao FROM clientes WHERE id = ?",
            (cliente_id,)
        ).fetchone()
        conn.close()
        if not row or not row[0]:
            return True
        venc = datetime.date.fromisoformat(row[0])
        return venc < datetime.date.today()
