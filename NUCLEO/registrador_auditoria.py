import json
import os
from datetime import datetime

PASTA_AUDITORIA = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\AUDITORIA"

os.makedirs(PASTA_AUDITORIA, exist_ok=True)

def registrar(evento, dados):
    registro = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": evento,
        "dados": dados
    }

    nome = datetime.now().strftime("%Y%m%d_%H%M%S") + "_auditoria.json"
    caminho = os.path.join(PASTA_AUDITORIA, nome)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(registro, f, indent=2, ensure_ascii=False)

    return caminho