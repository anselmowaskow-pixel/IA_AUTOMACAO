# ==========================================================
# SERVIDOR PROFISSIONAL PRÓ+++ - IA_AUTOMACAO
# ==========================================================

from flask import Flask, render_template, send_file
import os
import csv

app = Flask(__name__)

BASE_STORAGE = r"C:\IA_AUTOMACAO\STORAGE"


# ==========================================================
# LIMPEZA DE DADOS
# ==========================================================

def limpar(valor):
    if valor in [None, "", "None"]:
        return "-"
    return valor


# ==========================================================
# CARREGAR EVENTOS
# ==========================================================

def carregar_eventos(empresa):

    caminho = os.path.join(
        BASE_STORAGE,
        empresa,
        "AUDITORIA",
        "EVENTOS_EMPRESA.csv"
    )

    eventos = []

    if not os.path.exists(caminho):
        return eventos

    with open(caminho, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            eventos.append(row)

    return eventos


# ==========================================================
# TRATAR EVENTOS
# ==========================================================

def preparar_eventos(eventos):

    lista = []

    for e in eventos:

        lista.append({
            "data": limpar(e.get("data")),
            "hora": limpar(e.get("hora")),
            "documento": limpar(e.get("numero_documento")),
            "tipo": limpar(e.get("tipo_documento")),
            "operacao": limpar(e.get("natureza_operacao")),
            "status": limpar(e.get("status")),
            "acao": limpar(e.get("acao")),
            "valor": limpar(e.get("valor_total")),
            "arquivo": limpar(e.get("arquivo"))
        })

    return list(reversed(lista))  # mais recente primeiro


# ==========================================================
# RESUMO (CARDS)
# ==========================================================

def resumo(eventos):

    return {
        "total": len(eventos),
        "ok": sum(1 for e in eventos if e["status"] == "OK"),
        "erro": sum(1 for e in eventos if e["status"] == "ERRO"),
        "ilegivel": sum(1 for e in eventos if e["status"] == "ILEGIVEL"),
        "duplicado": sum(1 for e in eventos if e["status"] == "DUPLICADO"),
        "nao_fiscal": sum(1 for e in eventos if e["status"] == "NAO_FISCAL"),
    }


# ==========================================================
# LOCALIZAR PDF
# ==========================================================

def localizar_pdf(empresa, nome_arquivo):

    base = os.path.join(BASE_STORAGE, empresa)

    for raiz, dirs, arquivos in os.walk(base):
        if nome_arquivo in arquivos:
            return os.path.join(raiz, nome_arquivo)

    return None


# ==========================================================
# ROTA PRINCIPAL
# ==========================================================

@app.route("/")
def painel():

    empresa = "Empresa_TESTE"  # pode depois tornar dinâmico

    eventos_raw = carregar_eventos(empresa)
    eventos = preparar_eventos(eventos_raw)

    dados_resumo = resumo(eventos)

    return render_template(
        "painel_empresa.html",
        eventos=eventos,
        resumo=dados_resumo,
        empresa=empresa
    )


# ==========================================================
# ABRIR PDF
# ==========================================================

@app.route("/abrir/<arquivo>")
def abrir(arquivo):

    empresa = "Empresa_TESTE"

    caminho = localizar_pdf(empresa, arquivo)

    if caminho and os.path.exists(caminho):
        return send_file(caminho)

    return "Arquivo não encontrado"


# ==========================================================
# START
# ==========================================================

if __name__ == "__main__":
    print("🚀 SERVIDOR PRÓ+++ RODANDO...")
    app.run(debug=True)