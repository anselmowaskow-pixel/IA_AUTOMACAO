import json
import os

CAMINHO_REGRAS_FISCAIS = os.path.join(
    os.path.dirname(__file__),
    "regras_fiscais.json"
)

def carregar_regras_fiscais():
    with open(CAMINHO_REGRAS_FISCAIS, "r", encoding="utf-8") as f:
        return json.load(f)