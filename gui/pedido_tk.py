import os
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime

# Ajusta path para pacotes internos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.db import get_connection
from printer.escpos_service import print_order


def run_pedido(cliente_id: int):
    """
    Tela de registro e impressão (geração de PDF) de pedido em Tkinter.
    :param cliente_id: ID do cliente que faz o pedido.
    """
    # Busca dados do cliente
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT nome, endereco, telefone FROM clientes WHERE id = ?", (cliente_id,)
    ).fetchone()
    conn.close()

    nome, endereco, telefone = row

    # Inicializa janela
    root = tk.Tk()
    root.title("PizzariaApp - Pedido")
    root.geometry("400x350")

    # Informações do cliente
    tk.Label(root, text=f"Cliente: {nome}").pack(anchor='w', padx=10, pady=5)
    tk.Label(root, text=f"Telefone: {telefone}").pack(anchor='w', padx=10)
    tk.Label(root, text=f"Endereço: {endereco}").pack(anchor='w', padx=10, pady=5)

    # Campo Sabor
    tk.Label(root, text="Sabor:").pack(anchor='w', padx=10)
    sabor_var = tk.StringVar()
    tk.Entry(root, textvariable=sabor_var, width=30).pack(anchor='w', padx=10)

    # Campo Quantidade
    tk.Label(root, text="Quantidade:").pack(anchor='w', padx=10, pady=5)
    qtde_var = tk.IntVar(value=1)
    tk.Spinbox(root, from_=1, to=100, textvariable=qtde_var, width=5).pack(anchor='w', padx=10)

    # Campo Observações
    tk.Label(root, text="Observações:").pack(anchor='w', padx=10, pady=5)
    obs_text = scrolledtext.ScrolledText(root, width=40, height=5)
    obs_text.pack(padx=10)

    def salvar_e_imprimir():
        """
        Valida, salva o pedido no banco e gera um PDF do pedido.
        Em seguida, retorna à tela principal.
        """
        sabor = sabor_var.get().strip()
        quantidade = qtde_var.get()
        observacoes = obs_text.get('1.0', tk.END).strip()

        if not sabor:
            messagebox.showerror("Erro", "Informe o sabor.", parent=root)
            return

        # Salvar no DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, sabor, quantidade, observacoes) VALUES (?,?,?,?)",
            (cliente_id, sabor, quantidade, observacoes)
        )
        conn.commit()
        conn.close()

        # Gerar PDF
        try:
            pdf_path = print_order(
                nome=nome,
                telefone=telefone,
                endereco=endereco,
                sabor=sabor,
                quantidade=quantidade,
                observacoes=observacoes
            )
            messagebox.showinfo(
                "Sucesso",
                f"Pedido salvo e PDF gerado em:\n{pdf_path}",
                parent=root
            )
        except Exception as e:
            messagebox.showerror("Erro de impressão", str(e), parent=root)

                # Fecha janela de pedido
        root.destroy()
        # Volta para a tela principal diretamente
        import gui.principal_tk as principal_tk
        principal_tk.run_main(cliente_id)

    # Botões
    tk.Button(root, text="Imprimir Pedido", width=15, command=salvar_e_imprimir).pack(pady=15)
    tk.Button(root, text="Cancelar", width=15, command=lambda: root.destroy()).pack()

    root.mainloop()


if __name__ == "__main__":
    # Para teste isolado, substitua 1 pelo ID de um cliente
    run_pedido(1)
