import os
import json
from datetime import datetime

EMPRESA = "Empresa A"

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa A"
PROCESSADOS = os.path.join(BASE, "PROCESSADOS")
RESULTADOS = os.path.join(BASE, "RESULTADOS")

os.makedirs(RESULTADOS, exist_ok=True)

def gerar_resultado(arquivo):
    nome_json = arquivo + ".json"
    caminho_json = os.path.join(RESULTADOS, nome_json)

    if os.path.exists(caminho_json):
        return  # já gerado

    dados = {
        "empresa": EMPRESA,
        "arquivo": arquivo,
        "tipo": os.path.splitext(arquivo)[1].replace(".", "").upper(),
        "status": "PROCESSADO",
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origem": os.path.join(BASE, "ENTRADA"),
        "destino": PROCESSADOS
    }

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def executar():
    for arquivo in os.listdir(PROCESSADOS):
        if arquivo.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            gerar_resultado(arquivo)

if __name__ == "__main__":
    executar()
    print("RESULTADOS GERADOS COM SUCESSO")