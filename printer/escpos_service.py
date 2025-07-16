import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Diretório onde os PDFs serão salvos
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'orders'))
os.makedirs(OUTPUT_DIR, exist_ok=True)


def print_order(nome: str, telefone: str, endereco: str, sabor: str, quantidade: int, observacoes: str) -> str:
    """
    Gera um PDF com o pedido do cliente.
    Retorna o caminho do arquivo gerado.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'pedido_{timestamp}.pdf'
    filepath = os.path.join(OUTPUT_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, height - 50, 'PEDIDO PIZZARIA XYZ')

    # Dados do cliente
    c.setFont('Helvetica', 12)
    c.drawString(50, height - 80, f'Cliente: {nome}')
    c.drawString(50, height - 100, f'Telefone: {telefone}')
    c.drawString(50, height - 120, f'Endereço: {endereco}')

    # Detalhes do pedido
    c.drawString(50, height - 160, 'Sabor:')
    c.drawString(120, height - 160, sabor)
    c.drawString(50, height - 180, 'Quantidade:')
    c.drawString(150, height - 180, str(quantidade))

    # Observações
    c.drawString(50, height - 220, 'Observações:')
    text_obj = c.beginText(50, height - 240)
    for line in observacoes.splitlines():
        text_obj.textLine(line)
    c.drawText(text_obj)

    # Rodapé
    c.drawString(50, 50, f'Data: {datetime.now().isoformat()}')

    c.showPage()
    c.save()
    return filepath
