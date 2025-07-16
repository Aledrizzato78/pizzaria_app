import sys
import PySimpleGUI as sg
from data.db import get_connection


def run_cadastro():
    """
    Executa a tela de cadastro de um novo cliente.
    """
    sg.theme('LightGreen')
    layout = [
        [sg.Text('Nome:'), sg.Input(key='nome', size=(30, 1))],
        [sg.Text('Telefone:'), sg.Input(key='telefone', size=(20, 1))],
        [sg.Text('Endereço:'), sg.Input(key='endereco', size=(40, 1))],
        [sg.Button('Salvar'), sg.Button('Cancelar')]
    ]

    window = sg.Window('PizzariaApp - Cadastro de Cliente', layout)

    while True:
        ev, vals = window.read()
        if ev in (sg.WIN_CLOSED, 'Cancelar'):
            window.close()
            sys.exit(0)
        if ev == 'Salvar':
            nome = vals['nome'].strip()
            telefone = vals['telefone'].strip()
            endereco = vals['endereco'].strip()

            if not nome or not telefone:
                sg.popup_error('Nome e telefone são obrigatórios!')
                continue

            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO clientes (nome, telefone, endereco, data_vencimento_locacao) VALUES (?, ?, ?, ?)" ,
                    (nome, telefone, endereco, None)
                )
                conn.commit()
                sg.popup('Cliente cadastrado com sucesso!')
                window.close()
                return
            except Exception as e:
                sg.popup_error(f'Erro ao cadastrar cliente: {e}')
                conn.rollback()
            finally:
                conn.close()
