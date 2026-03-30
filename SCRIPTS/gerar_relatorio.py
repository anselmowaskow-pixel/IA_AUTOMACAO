# -*- coding: utf-8 -*-
import os
import json
import csv

BASE = r"C:\IA_AUTOMACAO\STORAGE"
EMPRESA = "Empresa A"

RESULTADOS = os.path.join(BASE, EMPRESA, "RESULTADOS")
SAIDA = os.path.join(RESULTADOS, "relatorio_empresaA.csv")

campos = [
    "tipo",
    "numero",
    "emitente",
    "cnpj_emitente",
    "valor_total",
    "chave"
]

linhas = []

for arquivo in os.listdir(RESULTADOS):
    if arquivo.endswith(".json"):
        caminho = os.path.join(RESULTADOS, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        linha = {campo: dados.get(campo, "") for campo in campos}
        linhas.append(linha)

with open(SAIDA, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=campos, delimiter=";")
    writer.writeheader()
    writer.writerows(linhas)

print("RELATORIO GERADO:", SAIDA)