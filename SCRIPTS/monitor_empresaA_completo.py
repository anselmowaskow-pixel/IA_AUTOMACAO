import os
import time
import json
from extrator_xml import extrair_dados_xml

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa A"
ENTRADA = os.path.join(BASE, "PASTA_ENTRADA")
SAIDA = os.path.join(BASE, "RESULTADOS")

os.makedirs(SAIDA, exist_ok=True)
processados = set()

print("Monitor Empresa A ATIVO...")

while True:
    for nome in os.listdir(ENTRADA):
        if not nome.lower().endswith(".xml"):
            continue

        caminho = os.path.join(ENTRADA, nome)
        if caminho in processados:
            continue

        try:
            dados = extrair_dados_xml(caminho)
            saida_json = os.path.join(SAIDA, nome + ".json")

            with open(saida_json, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)

            print("OK ->", saida_json)
            processados.add(caminho)

        except Exception as e:
            print("ERRO:", nome, e)
            processados.add(caminho)

    time.sleep(2)