import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import PySimpleGUI as sg
from license.validator import LicenseValidator
from data.db import get_connection

# Configuração da SECRET_KEY (deve coincidir com LicenseGenerator)
SECRET_KEY = b'minha_chave_secreta'


class GUIStartup:
    """
    Classe responsável por iniciar o aplicativo:
    - Verifica se o cliente existe e se a licença está válida.
    - Redireciona para a tela principal ou tela de licença expirada.
    """

    def __init__(self, cliente_id: int=1):
        self.cliente_id = cliente_id
        self.validator = LicenseValidator(SECRET_KEY)

    def run(self):
        # Verifica expiração
        if self.validator.is_expired(self.cliente_id):
            self.show_expired_screen()
        else:
            self.show_main_screen()

    def show_expired_screen(self):
        # usando tema padrão do PySimpleGUI
        layout = [
            [sg.Text('Licença Expirada!', font=('Any', 20), text_color='red')],
            [sg.Text('Sua licença venceu. Por favor, renove.')],
            [sg.Button('Administrar Licença'), sg.Button('Sair')]
        ]
        window = sg.Window('PizzariaApp - Licença', layout)
        while True:
            ev, _ = window.read()
            if ev in (sg.WIN_CLOSED, 'Sair'):
                window.close()
                sys.exit(0)
            if ev == 'Administrar Licença':
                window.close()
                import gui.admin as admin_module
                admin_module.run_admin(self.cliente_id)
                # após administração, reinicia startup
                GUIStartup(self.cliente_id).run()
                return

    def show_main_screen(self):
        # fecha janela anterior caso exista
        try:
            window.close()
        except:
            pass
        import gui.principal as main_module
        main_module.run_main(self.cliente_id)


if __name__ == '__main__':
    # Exemplo: define ID do cliente (fixo 1 para teste)
    GUIStartup(cliente_id=1).run()
