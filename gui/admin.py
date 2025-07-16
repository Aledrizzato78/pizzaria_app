import sys
import PySimpleGUI as sg
from license.validator import LicenseValidator

# Configuração da SECRET_KEY (mesma do startup)
SECRET_KEY = b'minha_chave_secreta'
ADMIN_PASSWORD = 'admin123'  # ajuste conforme necessidade


def run_admin(cliente_id: int):
    """
    Executa a tela de administração de licença.
    Solicita senha de administrador e, em seguida, o código de licença.
    Valida e atualiza o vencimento.
    """
    validator = LicenseValidator(SECRET_KEY)

    # Passo 1: senha
    sg.theme('DarkGrey5')
    layout_pass = [
        [sg.Text('Senha de Admin:'), sg.Input(password_char='*', key='senha')],
        [sg.Button('Entrar'), sg.Button('Cancelar')]
    ]
    win_pass = sg.Window('Administração - Login', layout_pass)
    while True:
        ev, vals = win_pass.read()
        if ev in (sg.WIN_CLOSED, 'Cancelar'):
            win_pass.close()
            sys.exit(0)
        if ev == 'Entrar':
            if vals['senha'] != ADMIN_PASSWORD:
                sg.popup_error('Senha incorreta!')
                continue
            break
    win_pass.close()

    # Passo 2: código de licença
    layout_code = [
        [sg.Text('Código de Licença:'), sg.Input(key='code', size=(40, 1))],
        [sg.Button('Validar e Renovar'), sg.Button('Cancelar')]
    ]
    win_code = sg.Window('Administração - Licença', layout_code)
    while True:
        ev, vals = win_code.read()
        if ev in (sg.WIN_CLOSED, 'Cancelar'):
            win_code.close()
            sys.exit(0)
        if ev == 'Validar e Renovar':
            code = vals['code']
            try:
                exp_date = validator.validate_and_update(cliente_id, code)
                sg.popup('Licença renovada até', exp_date.isoformat())
                win_code.close()
                return
            except Exception as e:
                sg.popup_error(f'Erro: {e}')
                continue
