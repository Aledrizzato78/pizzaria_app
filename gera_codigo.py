# gera_codigo.py

import datetime
from license.generator import LicenseGenerator

# Use EXATAMENTE a mesma chave secreta que o app usa:
SECRET_KEY = b'minha_chave_secreta'


def main():
    gen = LicenseGenerator(SECRET_KEY)
    # Define a data de expiração desejada: hoje + 30 dias
    novo_venc = datetime.date.today() + datetime.timedelta(days=30)
    codigo = gen.generate_code(novo_venc)
    print("Código de Licença (expira em", novo_venc.isoformat() + "):")
    print(codigo)


if __name__ == "__main__":
    main()
