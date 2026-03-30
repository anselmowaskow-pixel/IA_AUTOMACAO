# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
import shutil

EMPRESA = "Empresa A"
CONTADOR = "Contador B"

ORIGEM = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\RESULTADOS"
DESTINO = r"C:\IA_AUTOMACAO\STORAGE\ENTREGAS"

os.makedirs(DESTINO, exist_ok=True)

entrega = {
    "empresa": EMPRESA,
    "contador": CONTADOR,
    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "arquivos": []
}

for arq in os.listdir(ORIGEM):
    if arq.endswith(".json"):
        origem_arq = os.path.join(ORIGEM, arq)
        nome_saida = f"{EMPRESA.replace(' ','_')}_{arq}"
        destino_arq = os.path.join(DESTINO, nome_saida)

        shutil.copy2(origem_arq, destino_arq)
        entrega["arquivos"].append(nome_saida)

relatorio = os.path.join(DESTINO, f"entrega_{EMPRESA.replace(' ','_')}.json")

with open(relatorio, "w", encoding="utf-8") as f:
    json.dump(entrega, f, indent=2, ensure_ascii=False)

print("ENTREGA GERADA COM SUCESSO")