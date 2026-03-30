import json
import re

def validar_nfe(dados):
    erros = []

    # numero da nota
    if not dados.get("numero"):
        erros.append("numero_da_nota_ausente")

    # cnpj
    cnpj = dados.get("cnpj_emitente", "")
    if not re.fullmatch(r"\d{14}", cnpj):
        erros.append("cnpj_emitente_invalido")

    # valor total
    try:
        valor = float(dados.get("valor_total", "0"))
        if valor <= 0:
            erros.append("valor_total_invalido")
    except:
        erros.append("valor_total_nao_numerico")

    status = "APROVADO" if not erros else "REPROVADO"

    return {
        "status_fiscal": status,
        "erros": erros,
        "dados_nfe": dados
    }

if __name__ == "__main__":
    with open("entrada_nfe.json", encoding="utf-8") as f:
        dados = json.load(f)

    resultado = validar_nfe(dados)

    with open("resultado_validacao.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print("VALIDACAO CONCLUIDA:", resultado["status_fiscal"])