import json
import os
from datetime import datetime

ARQ_PRODUTOS = "STORAGE/produtos.json"
ARQ_SAIDAS = "STORAGE/saidas.json"

def carregar_json(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def saida_produto(
    empresa_id,
    produto_id,
    quantidade,
    valor_unitario,
    observacao=""
):
    produtos = carregar_json(ARQ_PRODUTOS)
    saidas = carregar_json(ARQ_SAIDAS)

    produto = next(
        (p for p in produtos if p["id"] == produto_id and p["empresa_id"] == empresa_id),
        None
    )

    if not produto:
        print("Produto nao encontrado para esta empresa")
        return

    if produto["estoque"] < int(quantidade):
        print("Estoque insuficiente")
        print("Disponivel:", produto["estoque"])
        return

    produto["estoque"] -= int(quantidade)

    saida = {
        "id": len(saidas) + 1,
        "empresa_id": empresa_id,
        "produto_id": produto_id,
        "quantidade": quantidade,
        "valor_unitario": float(valor_unitario),
        "valor_total": float(quantidade) * float(valor_unitario),
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "observacao": observacao
    }

    saidas.append(saida)

    salvar_json(ARQ_PRODUTOS, produtos)
    salvar_json(ARQ_SAIDAS, saidas)

    print("Venda registrada com sucesso")
    print("Estoque atual:", produto["estoque"])

# ===== EXECUÇÃO DIRETA =====
if __name__ == "__main__":
    saida_produto(
        empresa_id=11,
        produto_id=1,
        quantidade=5,
        valor_unitario=15.00,
        observacao="Venda balcão"
    )
