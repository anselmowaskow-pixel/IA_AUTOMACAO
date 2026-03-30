# -*- coding: utf-8 -*-

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa A"
ARQUIVO_JSON = os.path.join(BASE, "relatorio_empresaA.json")
ARQUIVO_PDF = os.path.join(BASE, "relatorio_empresaA.pdf")

def gerar_pdf():
    if not os.path.exists(ARQUIVO_JSON):
        print("ERRO: relatorio_empresaA.json nao encontrado")
        return

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # NORMALIZACAO: se nao for lista, transforma em lista
    if isinstance(dados, dict):
        dados = [dados]
    elif isinstance(dados, str):
        dados = [{"texto": dados}]

    c = canvas.Canvas(ARQUIVO_PDF, pagesize=A4)
    largura, altura = A4

    y = altura - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "RELATORIO - EMPRESA A")
    y -= 30

    c.setFont("Helvetica", 10)

    total_notas = 0
    valor_total = 0.0

    for item in dados:
        numero = item.get("numero", "")
        emitente = item.get("emitente", "")
        valor = item.get("valor_total", "0")

        linha = f"NF {numero} | {emitente} | R$ {valor}"
        c.drawString(50, y, linha)
        y -= 15

        total_notas += 1
        try:
            valor_total += float(valor)
        except:
            pass

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = altura - 50

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, f"TOTAL DE NOTAS: {total_notas}")
    y -= 15
    c.drawString(50, y, f"VALOR TOTAL: R$ {valor_total:.2f}")

    c.save()
    print("PDF GERADO COM SUCESSO:", ARQUIVO_PDF)

if __name__ == "__main__":
    gerar_pdf()