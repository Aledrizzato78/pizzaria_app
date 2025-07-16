# pizzaria_app/gui/principal_tk.py

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Ajusta path para pacotes internos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.db import get_connection
import gui.cadastro_tk as cadastro_tk
import gui.pedido_tk as pedido_tk


def run_main(cliente_id: int):
    """
    Tela principal em Tkinter:
    - Busca cliente por telefone
    - Exibe nome e endereço
    - Botões: Buscar, Novo Cliente, Fazer Pedido, Histórico, Sair
    """
    # Inicializa janela
    root = tk.Tk()
    root.title("PizzariaApp - Principal")
    root.geometry("400x250")

    # Widgets
    tk.Label(root, text="Telefone:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    telefone_var = tk.StringVar()
    tk.Entry(root, textvariable=telefone_var).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Buscar", width=10,
              command=lambda: buscar()).grid(row=0, column=2, padx=5)
    tk.Button(root, text="Novo Cliente", width=10,
              command=lambda: novo_cliente()).grid(row=0, column=3, padx=5)

    tk.Label(root, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    nome_var = tk.StringVar()
    tk.Entry(root, textvariable=nome_var, state='readonly', width=40).grid(row=1, column=1, columnspan=3, padx=5)

    tk.Label(root, text="Endereço:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    endereco_var = tk.StringVar()
    tk.Entry(root, textvariable=endereco_var, state='readonly', width=40).grid(row=2, column=1, columnspan=3, padx=5)

    # Botões inferiores
    tk.Button(root, text="Fazer Pedido", width=12,
              command=lambda: fazer_pedido()).grid(row=4, column=1, pady=15)
    tk.Button(root, text="Histórico", width=12,
              command=lambda: mostrar_historico()).grid(row=4, column=2)
    tk.Button(root, text="Sair", width=12,
              command=lambda: root.destroy()).grid(row=4, column=3)

    cliente_db_id = None  # ID do cliente encontrado

    def buscar():
        nonlocal cliente_db_id
        tel = telefone_var.get().strip()
        if not tel:
            messagebox.showwarning("Aviso", "Digite um telefone!")
            return
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute(
            'SELECT id, nome, endereco FROM clientes WHERE telefone = ?',
            (tel,)
        ).fetchone()
        conn.close()
        if row:
            cliente_db_id, nome, endereco = row
            nome_var.set(nome)
            endereco_var.set(endereco)
        else:
            messagebox.showinfo("Não encontrado", "Cliente não cadastrado.")
            nome_var.set("")
            endereco_var.set("")
            cliente_db_id = None

    def novo_cliente():
        root.destroy()
        cadastro_tk.run_cadastro()  # após cadastro, retorna aqui?
        run_main(cliente_id)

    def fazer_pedido():
        if cliente_db_id:
            root.destroy()
            pedido_tk.run_pedido(cliente_db_id)
        else:
            messagebox.showwarning("Aviso", "Busque um cliente antes de pedir.")

    def mostrar_historico():
        messagebox.showinfo("Histórico", "Funcionalidade não implementada.")

    root.mainloop()
