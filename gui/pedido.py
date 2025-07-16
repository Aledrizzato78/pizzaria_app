import sys
import PySimpleGUI as sg
from data.db import get_connection
from printer.escpos_service import print_order


def run_pedido(cliente_id: int):
    """
    Executa a tela de registro e impressão de pedido.
    :param cliente_id: ID do cliente que faz o pedido.
    """
    # Fetch client info
    conn = get_connection()
    cursor = conn.cursor()
    nome, endereco, telefone = cursor.execute(
        "SELECT nome, endereco, telefone FROM clientes WHERE id = ?", (cliente_id,)
    ).fetchone()
    conn.close()

    sg.theme('LightYellow')
    layout = [
        [sg.Text(f'Cliente: {nome}'), sg.Text(f'Fone: {telefone}')],
        [sg.Text(f'Endereço: {endereco}')],
        [sg.Text('Sabor:'), sg.Input(key='sabor', size=(30, 1))],
        [sg.Text('Quantidade:'), sg.Input(default_text='1', key='qtde', size=(5, 1))],
        [sg.Text('Observações:'), sg.Multiline(key='obs', size=(40, 3))],
        [sg.Button('Imprimir Pedido'), sg.Button('Cancelar')]
    ]

    window = sg.Window('PizzariaApp - Pedido', layout)

    while True:
        ev, vals = window.read()
        if ev in (sg.WIN_CLOSED, 'Cancelar'):
            break
        if ev == 'Imprimir Pedido':
            sabor = vals['sabor'].strip()
            try:
                quantidade = int(vals['qtde'])
            except ValueError:
                sg.popup_error('Quantidade deve ser número inteiro!')
                continue
            obs = vals['obs'].strip()

            if not sabor or quantidade < 1:
                sg.popup_error('Informe sabor e quantidade >= 1')
                continue

            # Salvar no DB
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pedidos (cliente_id, sabor, quantidade, observacoes) VALUES (?, ?, ?, ?)",
                (cliente_id, sabor, quantidade, obs)
            )
            conn.commit()
            conn.close()

            # Imprimir via ESC/POS
            try:
                print_order(
                    nome=nome,
                    telefone=telefone,
                    endereco=endereco,
                    sabor=sabor,
                    quantidade=quantidade,
                    observacoes=obs
                )
                sg.popup('Pedido impresso com sucesso!')
            except Exception as e:
                sg.popup_error(f'Erro ao imprimir: {e}')

    window.close()
    # Retorna ao principal ao final
    sys.exit(0)
