# pizzaria_app/gui/startup_tk.py

import os
import sys
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Ajusta path para pacotes internos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from license.validator import LicenseValidator

# Configurações
SECRET_KEY = b'minha_chave_secreta'
ADMIN_PASSWORD = 'admin123'  # mesmo que no admin_tk.py


class StartupApp:

    def __init__(self, cliente_id=1):
        self.cliente_id = cliente_id
        self.validator = LicenseValidator(SECRET_KEY)
        self.root = tk.Tk()
        self.root.title("PizzariaApp")

        # Decide qual tela mostrar
        if self.validator.is_expired(self.cliente_id):
            self.show_expired()
        else:
            self.show_main()

    def show_expired(self):
        # Alerta de licença expirada
        messagebox.showwarning(
            "Licença Expirada",
            "Sua licença venceu. Renove para continuar."
        )
        # Pergunta se quer administrar licença agora
        renovar = messagebox.askyesno(
            "Administrar Licença",
            "Deseja inserir código de licença agora?"
        )
        if renovar:
            # Chama o fluxo de admin em Tkinter
            self.root.destroy()
            import gui.admin_tk as admin_tk
            admin_tk.run_admin_tk(self.cliente_id)
            # Após admin, reinicia a aplicação
            StartupApp(self.cliente_id).run()
        else:
            self.root.destroy()
            sys.exit(0)

    def show_main(self):
        # Fecha a janela de startup
        self.root.destroy()
        # Importa e executa a GUI principal em Tkinter
        import gui.principal_tk as main_tk
        main_tk.run_main(self.cliente_id)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StartupApp(cliente_id=1)
    app.run()
