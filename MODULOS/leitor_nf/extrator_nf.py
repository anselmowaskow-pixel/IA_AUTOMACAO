# -*- coding: utf-8 -*-
import re
import json

def extrair_dados(texto):
    texto = texto.upper()

    dados = {
        "tipo": "NFE",
        "numero": "",
        "chave": "",
        "emitente": "",
        "valor_total": "",
        "cnpj_emitente": "",
        "data_emissao": "",
        "produto": ""
    }

    # Numero da nota
    num = re.search(r"\bN\s*\.?\s*(\d{8,12})", texto)
    if not num:
        num = re.search(r"\b(\d{8,12})\b", texto)
    if num:
        dados["numero"] = num.group(1)

    # Chave de acesso
    chave = re.search(r"\b(\d{44})\b", texto)
    if chave:
        dados["chave"] = chave.group(1)

    # Emitente (nome)
    emit = re.search(r"\b([A-Z]{4,})\b", texto)
    if emit:
        dados["emitente"] = emit.group(1)

    # Valor total
    valor = re.search(r"\bTOTAL\s*(\d+[\,\.]\d+)", texto)
    if valor:
        dados["valor_total"] = valor.group(1)

    # CNPJ
    cnpj = re.search(r"\b(\d{14})\b", texto)
    if cnpj:
        dados["cnpj_emitente"] = cnpj.group(1)

    # Produto (apenas exemplo)
    if "TABACO" in texto:
        dados["produto"] = "TABACO"

    # Data emissao simples (formato DD/MM/AAAA)
    data = re.search(r"\b(\d{2}\/\d{2}\/\d{4})\b", texto)
    if data:
        dados["data_emissao"] = data.group(1)

    return dados

if __name__ == "__main__":
    with open("texto_nf.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    dados = extrair_dados(texto)
    print(json.dumps(dados, indent=2))