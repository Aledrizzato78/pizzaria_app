import sys
import PySimpleGUI as sg
from data.db import get_connection
import gui.cadastro as cadastro_module
import gui.pedido as pedido_module


def run_main(cliente_id: int):
    """
    Executa a tela principal: busca/cadastro de cliente e navega para pedido ou cadastro.
    :param cliente_id: ID fixo de cliente para verificação de licença (não usado aqui diretamente).
    """
    sg.theme('LightBlue')
    layout = [
        [sg.Text('Telefone:'), sg.Input(key='telefone', size=(20, 1)), sg.Button('Buscar'), sg.Button('Novo Cliente')],
        [sg.Text('Nome:'), sg.Input(key='nome', disabled=True, size=(30, 1))],
        [sg.Text('Endereço:'), sg.Input(key='endereco', disabled=True, size=(30, 1))],
        [sg.HorizontalSeparator()],
        [sg.Button('Fazer Pedido'), sg.Button('Histórico'), sg.Button('Sair')]
    ]

    window = sg.Window('PizzariaApp - Principal', layout)
    cliente_db_id = None

    while True:
        ev, vals = window.read()
        if ev in (sg.WIN_CLOSED, 'Sair'):
            break

        conn = get_connection()
        c = conn.cursor()
        if ev == 'Buscar':
            tel = vals['telefone']
            row = c.execute('SELECT id, nome, endereco FROM clientes WHERE telefone = ?', (tel,)).fetchone()
            if row:
                cliente_db_id, nome, endereco = row
                window['nome'].update(nome)
                window['endereco'].update(endereco)
            else:
                sg.popup('Cliente não encontrado!')
                cliente_db_id = None
        elif ev == 'Novo Cliente':
            window.close()
            cadastro_module.run_cadastro()
            # Reopen main after cadastro
            run_main(cliente_id)
            return
        elif ev == 'Fazer Pedido':
            if not cliente_db_id:
                sg.popup('Busque um cliente antes de fazer o pedido!')
            else:
                window.close()
                pedido_module.run_pedido(cliente_db_id)
                # Após pedido, reabre principal
                run_main(cliente_id)
                return
        elif ev == 'Histórico':
            sg.popup('Funcionalidade de histórico ainda não implementada.')

        conn.close()

    window.close()
    sys.exit(0)
