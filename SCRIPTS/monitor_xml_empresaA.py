# -*- coding: utf-8 -*-
import os
import time
import xml.etree.ElementTree as ET
import json

ENTRADA = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\PASTA_ENTRADA"
SAIDA = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\RESULTADOS"

os.makedirs(ENTRADA, exist_ok=True)
os.makedirs(SAIDA, exist_ok=True)

def processar_xml(caminho):
    tree = ET.parse(caminho)
    root = tree.getroot()

    def get_text(tag):
        try:
            elem = root.find(tag)
            return elem.text if elem is not None else ""
        except:
            return ""

    dados = {
        "tipo": "NFE-XML",
        "numero": get_text(".//ide/nNF"),
        "emitente": get_text(".//emit/xNome"),
        "cnpj_emitente": get_text(".//emit/CNPJ"),
        "valor_total": get_text(".//total/vNF")
    }

    saida_json = os.path.join(SAIDA, os.path.basename(caminho) + ".json")
    with open(saida_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print("XML OK ->", saida_json)

def monitorar():
    print("Monitor XML Empresa A ATIVO...")
    processados = set()

    while True:
        for arquivo in os.listdir(ENTRADA):
            if arquivo.endswith(".xml"):
                caminho = os.path.join(ENTRADA, arquivo)

                if caminho not in processados:
                    processar_xml(caminho)
                    processados.add(caminho)

        time.sleep(2)

if __name__ == "__main__":
    monitorar()