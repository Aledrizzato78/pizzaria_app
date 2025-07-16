# pizzaria_app/gui/admin_tk.py

import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from license.validator import LicenseValidator

# Ajusta path para pacotes internos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mesma chave que você usa no generator/validator
SECRET_KEY = b'minha_chave_secreta'
ADMIN_PASSWORD = 'admin123'


def run_admin_tk(cliente_id: int):
    """
    Executa a janela de administração de licença em Tkinter:
    1) Pede senha de admin
    2) Se correta, pede o código de licença
    3) Valida, atualiza e exibe mensagem de sucesso ou erro
    """
    validator = LicenseValidator(SECRET_KEY)
    root = tk.Tk()
    root.withdraw()  # esconde a janela principal

    # 1) Pergunta senha
    pwd = simpledialog.askstring("Administração", "Senha de administrador:", show='*', parent=root)
    if pwd is None:
        sys.exit(0)
    if pwd != ADMIN_PASSWORD:
        messagebox.showerror("Erro", "Senha incorreta!", parent=root)
        root.destroy()
        sys.exit(0)

    # 2) Pergunta o código de licença
    code = simpledialog.askstring("Licença", "Cole o código de licença:", parent=root)
    if code is None:
        root.destroy()
        sys.exit(0)

    # 3) Valida e atualiza
    try:
        exp_date = validator.validate_and_update(cliente_id, code)
        messagebox.showinfo("Sucesso", f"Licença renovada até {exp_date.isoformat()}", parent=root)
    except Exception as e:
        messagebox.showerror("Erro ao validar código", str(e), parent=root)
        root.destroy()
        sys.exit(0)

    root.destroy()
