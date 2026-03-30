import json
import os
from datetime import datetime

ARQ_PRODUTOS = "STORAGE/produtos.json"

def criar_produto_auto(
    empresa_id,
    nome,
    sku,
    preco_custo,
    preco_venda,
    estoque_inicial=0
):
    if not os.path.exists("STORAGE"):
        os.makedirs("STORAGE")

    try:
        with open(ARQ_PRODUTOS, "r", encoding="utf-8") as f:
            produtos = json.load(f)
    except:
        produtos = []

    novo_id = max([p["id"] for p in produtos], default=0) + 1

    produto = {
        "id": novo_id,
        "empresa_id": empresa_id,
        "nome": nome.upper(),
        "sku": sku.upper(),
        "preco_custo": float(preco_custo),
        "preco_venda": float(preco_venda),
        "estoque": int(estoque_inicial),
        "ativo": True,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    produtos.append(produto)

    with open(ARQ_PRODUTOS, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

    print("Produto criado com sucesso:")
    print(produto)

# ===== EXECUÇÃO AUTOMÁTICA =====
if __name__ == "__main__":
    criar_produto_auto(
        empresa_id=11,           # ID da empresa
        nome="PRODUTO TESTE",
        sku="PROD-001",
        preco_custo=10.50,
        preco_venda=19.90,
        estoque_inicial=100
    )
