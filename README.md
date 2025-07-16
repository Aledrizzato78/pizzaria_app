# PizzeriaApp 🍕🖥️

![CI](https://github.com/Aledrizzato78/pizzaria_app/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.10%2B-blue)

> Sistema desktop leve para gerenciar pedidos de pizzaria, feito em **Python**, **Tkinter** e **SQLite**.

---

## 🚀 Funcionalidades

* 🔍 **Buscar cliente** por telefone
* ➕ **Cadastrar cliente** na interface
* 📝 **Formulário de pedido** (sabor, quantidade, observações)
* 🖨️ **Gerar PDF** do pedido via ReportLab
* 📂 **Histórico** salvo em `orders/` para consultas

---

## 🛠️ Tech Stack

| Camada         | Tecnologia              |
| -------------- | ----------------------- |
| Linguagem      | Python 3.x              |
| GUI            | Tkinter                 |
| Banco de dados | SQLite                  |
| PDF            | ReportLab               |
| Impressão      | escpos-python (ESC/POS) |

---

## 📁 Estrutura do Projeto

```bash
pizzaria_app/
├── .venv/
├── data/
│   ├── __init__.py
│   └── db.py
├── gui/
│   ├── __init__.py
│   ├── admin.py
│   ├── cadastro.py
│   ├── pedido.py
│   ├── principal.py
│   └── startup.py
├── license/
│   ├── __init__.py
│   ├── generator.py
│   └── validator.py
├── printer/
│   ├── __init__.py
│   └── escpos_service.py
│   └── orders/
├── main.py
├── requirements.txt
└── schema.sql
```

---

## 📥 Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/Aledrizzato78/pizzaria_app.git
   cd pizzaria_app
   ```
2. **Crie e ative o virtualenv**

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows
   # ou
   source venv/bin/activate       # macOS/Linux
   ```
3. **Instale dependências**

   ```bash
   pip install -r requirements.txt
   ```
4. **Rode o app**

   ```bash
   python main.py
   ```

---

## 📈 CI/CD (GitHub Actions)

Badge de CI acima — workflow definido em `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
      - name: Lint com flake8
        run: |
          source venv/bin/activate
          pip install flake8
          flake8 .
      - name: Run tests
        run: |
          source venv/bin/activate
          pytest --maxfail=1 --disable-warnings -q
```

---

## 🙌 Contribuições

1. Fork deste repositório
2. Crie uma branch `feature/nome-da-sua-ideia`
3. Commit suas mudanças (`git commit -m "feat: descrição da sua feature"`)
4. Push na branch (`git push origin feature/nome-da-sua-ideia`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está licenciado sob a [MIT License](./LICENSE).
