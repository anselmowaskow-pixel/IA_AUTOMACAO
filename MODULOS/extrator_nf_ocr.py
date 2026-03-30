import re
from datetime import datetime

def limpar_numero(txt):
    if not txt:
        return None
    return re.sub(r"\D", "", txt)

def extrair_primeiro(padrao, texto):
    achado = re.search(padrao, texto, re.MULTILINE)
    return achado.group(1).strip() if achado else None

def extrair_lista(padrao, texto):
    return re.findall(padrao, texto, re.MULTILINE)

def extrair_nf(texto_ocr):
    nf = {
        "tipo_documento": "NF-e",
        "chave_acesso": None,
        "numero_nf": None,
        "serie": None,
        "data_emissao": None,
        "emitente": {
            "cnpj": None,
            "razao_social": None
        },
        "destinatario": {
            "cpf_cnpj": None,
            "nome": None
        },
        "itens": [],
        "valor_total_nf": None,
        "status_leitura": "OCR_OK"
    }

    # CHAVE DE ACESSO (44 digitos)
    chaves = re.findall(r"\b\d{44}\b", texto_ocr)
    if chaves:
        nf["chave_acesso"] = chaves[0]

    # NUMERO NF
    nf["numero_nf"] = extrair_primeiro(
        r"N[ºo]\s*0*([0-9]{3,})",
        texto_ocr
    )

    # SERIE
    nf["serie"] = extrair_primeiro(
        r"S[EÉ]RIE\s*0*([0-9]+)",
        texto_ocr
    )

    # DATA EMISSAO
    datas = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texto_ocr)
    if datas:
        nf["data_emissao"] = datas[0]

    # CNPJ EMITENTE (14 digitos)
    cnpjs = re.findall(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b", texto_ocr)
    if cnpjs:
        nf["emitente"]["cnpj"] = limpar_numero(cnpjs[0])

    # CPF / CNPJ DESTINATARIO
    cpfs = re.findall(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", texto_ocr)
    if cpfs:
        nf["destinatario"]["cpf_cnpj"] = limpar_numero(cpfs[0])

    # RAZAO SOCIAL EMITENTE (heuristica simples)
    razao = extrair_primeiro(
        r"IDENTIFICAÇÃO DO EMITENTE\s+([A-Z0-9\.\s]+)",
        texto_ocr
    )
    if razao:
        nf["emitente"]["razao_social"] = razao

    # NOME DESTINATARIO
    nome_dest = extrair_primeiro(
        r"DESTINAT[AÁ]RIO\s*/\s*REMETENTE\s+([A-Z\s]+)",
        texto_ocr
    )
    if nome_dest:
        nf["destinatario"]["nome"] = nome_dest

    # ITENS (heuristica inicial)
    itens = re.findall(
        r"([A-Z\s]{5,})\s+\d{8}\s+\d{4}\s+\w+\s+([\d,]+)\s+([\d,]+)",
        texto_ocr
    )

    for it in itens:
        nf["itens"].append({
            "descricao": it[0].strip(),
            "quantidade": it[1],
            "valor_unitario": it[2]
        })

    # CLASSIFICACAO FINAL
    if not nf["chave_acesso"]:
        nf["status_leitura"] = "ILEGIVEL"
    elif not nf["emitente"]["cnpj"]:
        nf["status_leitura"] = "INCOMPLETA"

    return nf