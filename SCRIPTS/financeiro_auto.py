import json
import os
from datetime import datetime

ARQ_FINANCEIRO = "STORAGE/financeiro.json"

def carregar():
    try:
        with open(ARQ_FINANCEIRO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar(dados):
    with open(ARQ_FINANCEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def registrar_venda(
    empresa_id,
    origem,
    valor,
    forma_pagamento,
    status="RECEBIDO"
):
    financeiro = carregar()

    registro = {
        "id": len(financeiro) + 1,
        "empresa_id": empresa_id,
        "origem": origem,  # venda, servico, etc
        "valor": float(valor),
        "forma_pagamento": forma_pagamento,  # dinheiro pix cartao boleto
        "status": status,  # RECEBIDO ou A_RECEBER
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    financeiro.append(registro)
    salvar(financeiro)

    print("Financeiro registrado:", status)

def listar_financeiro(empresa_id):
    financeiro = carregar()

    total = 0
    pendente = 0

    for f in financeiro:
        if f["empresa_id"] == empresa_id:
            print(f)
            if f["status"] == "RECEBIDO":
                total += f["valor"]
            else:
                pendente += f["valor"]

    print("Total recebido:", total)
    print("Total pendente:", pendente)

# ===== EXECUÇÃO DIRETA =====
if __name__ == "__main__":
    registrar_venda(
        empresa_id=11,
        origem="Venda balcão",
        valor=75.00,
        forma_pagamento="PIX",
        status="RECEBIDO"
    )

    listar_financeiro(empresa_id=11)
