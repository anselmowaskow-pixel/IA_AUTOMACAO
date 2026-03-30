# -*- coding: utf-8 -*-
import os
import json
import csv

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa A"
RESULTADOS = os.path.join(BASE, "RESULTADOS")
SAIDA = os.path.join(BASE, "PASTA_SAIDA")

os.makedirs(SAIDA, exist_ok=True)

csv_saida = os.path.join(SAIDA, "relatorio_empresaA.csv")

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
    if not arquivo.endswith(".json"):
        continue

    caminho = os.path.join(RESULTADOS, arquivo)

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linha = {}
    for campo in campos:
        linha[campo] = dados.get(campo, "")

    linhas.append(linha)

with open(csv_saida, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=campos, delimiter=";")
    writer.writeheader()
    writer.writerows(linhas)

print("RELATORIO CSV GERADO COM SUCESSO")
print(csv_saida)