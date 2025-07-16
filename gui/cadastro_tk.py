# pizzaria_app/gui/cadastro_tk.py

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Ajusta path para pacotes internos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.db import get_connection


def run_cadastro():
    """
    Executa a janela de cadastro de cliente em Tkinter.
    """
    root = tk.Tk()
    root.title("Cadastro de Cliente")
    root.geometry("400x200")

    # Labels e Entradas
    tk.Label(root, text="Nome:").grid(row=0, column=0, padx=8, pady=8, sticky='e')
    nome_var = tk.StringVar()
    tk.Entry(root, textvariable=nome_var, width=40).grid(row=0, column=1)

    tk.Label(root, text="Telefone:").grid(row=1, column=0, padx=8, pady=8, sticky='e')
    telefone_var = tk.StringVar()
    tk.Entry(root, textvariable=telefone_var, width=25).grid(row=1, column=1)

    tk.Label(root, text="Endereço:").grid(row=2, column=0, padx=8, pady=8, sticky='e')
    endereco_var = tk.StringVar()
    tk.Entry(root, textvariable=endereco_var, width=40).grid(row=2, column=1)

    def salvar():
        nome = nome_var.get().strip()
        telefone = telefone_var.get().strip()
        endereco = endereco_var.get().strip()
        if not nome or not telefone:
            messagebox.showerror("Erro", "Nome e Telefone são obrigatórios.", parent=root)
            return
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO clientes (nome, telefone, endereco, data_vencimento_locacao) VALUES (?, ?, ?, ?)" ,
                (nome, telefone, endereco, None)
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!", parent=root)
            root.destroy()
        except Exception as e:
            messagebox.showerror("Erro ao cadastrar", str(e), parent=root)
        finally:
            conn.close()

    def cancelar():
        root.destroy()

    # Botões
    tk.Button(root, text="Salvar", width=12, command=salvar).grid(row=3, column=1, sticky='w', padx=8, pady=12)
    tk.Button(root, text="Cancelar", width=12, command=cancelar).grid(row=3, column=1, sticky='e', padx=8)

    root.mainloop()


if __name__ == "__main__":
    run_cadastro()
