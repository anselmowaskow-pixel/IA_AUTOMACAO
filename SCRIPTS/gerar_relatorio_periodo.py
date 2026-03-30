# -*- coding: utf-8 -*-
import os
import json
import csv
from datetime import datetime

BASE = r"C:\IA_AUTOMACAO\STORAGE"
EMPRESA = "Empresa A"

# AJUSTE O PERIODO AQUI
DATA_INICIO = "2025-01-01"
DATA_FIM    = "2025-12-31"

RESULTADOS = os.path.join(BASE, EMPRESA, "RESULTADOS")
SAIDA = os.path.join(RESULTADOS, "relatorio_periodo_empresaA.csv")

campos = [
    "tipo",
    "numero",
    "emitente",
    "cnpj_emitente",
    "valor_total",
    "chave",
    "data_emissao"
]

dt_ini = datetime.strptime(DATA_INICIO, "%Y-%m-%d")
dt_fim = datetime.strptime(DATA_FIM, "%Y-%m-%d")

linhas = []

for arquivo in os.listdir(RESULTADOS):
    if arquivo.endswith(".json"):
        caminho = os.path.join(RESULTADOS, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        data_str = dados.get("data_emissao", "")
        if not data_str:
            continue

        try:
            dt_doc = datetime.strptime(data_str, "%Y-%m-%d")
        except:
            continue

        if dt_ini <= dt_doc <= dt_fim:
            linha = {campo: dados.get(campo, "") for campo in campos}
            linhas.append(linha)

with open(SAIDA, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=campos, delimiter=";")
    writer.writeheader()
    writer.writerows(linhas)

print("RELATORIO POR PERIODO GERADO:", SAIDA)