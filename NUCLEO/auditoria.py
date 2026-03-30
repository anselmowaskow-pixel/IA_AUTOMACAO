# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

EMPRESA_ATIVA = "Empresa_A"

AUDITORIA_DIR = os.path.join(
    r"C:\IA_AUTOMACAO\STORAGE",
    EMPRESA_ATIVA,
    "AUDITORIA"
)
os.makedirs(AUDITORIA_DIR, exist_ok=True)

ARQUIVO_LOG = os.path.join(AUDITORIA_DIR, "auditoria.jsonl")

def registrar(evento):
    evento["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    # teste rapido
    registrar({
        "empresa": "Empresa A",
        "origem": "monitor_empresaA",
        "arquivo": "nota_teste.xml",
        "tipo": "XML",
        "status": "OK"
    })
    print("AUDITORIA OK")