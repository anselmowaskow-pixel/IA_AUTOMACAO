import re

def normalizar_texto(texto):
    if not texto:
        return ""
    return texto.upper()


def score(texto, palavras, peso=1):
    pontos = 0
    for p in palavras:
        if p in texto:
            pontos += peso
    return pontos


def classificar_documento(texto):

    texto = normalizar_texto(texto)

    score_nfce = 0
    score_nfe = 0
    score_cte = 0
    score_nfse = 0

    # ==========================================
    # NFC-e
    # ==========================================
    score_nfce += score(texto, [
        "NFC-E",
        "NFCE",
        "CONSUMIDOR ELETRON",
        "NOTA FISCAL DE CONSUMIDOR",
        "DOCUMENTO AUXILIAR"
    ], 2)

    if "SEFAZ" in texto and "QR" in texto:
        score_nfce += 2

    # ==========================================
    # NFE (DANFE)
    # ==========================================
    score_nfe += score(texto, [
        "DANFE",
        "NOTA FISCAL ELETRON",
        "CHAVE DE ACESSO",
        "PROTOCOLO DE AUTORIZACAO",
        "NATUREZA DA OPERACAO",
        "EMITENTE",
        "DESTINATARIO"
    ], 2)

    if re.search(r"\d{44}", texto):
        score_nfe += 4

    if "CNPJ" in texto:
        score_nfe += 1

    # ==========================================
    # CTE
    # ==========================================
    score_cte += score(texto, [
        "CONHECIMENTO DE TRANSPORTE",
        "CT-E",
        "DACTE"
    ], 3)

    # ==========================================
    # NFSE
    # ==========================================
    score_nfse += score(texto, [
        "NOTA FISCAL DE SERVI",
        "NFS-E",
        "NFSE"
    ], 3)

    # ==========================================
    # BOLETO
    # ==========================================
    if score(texto, ["BOLETO", "LINHA DIGITAVEL"], 2) >= 2:
        return "BOLETO"

    # ==========================================
    # RECIBO
    # ==========================================
    if "RECIBO" in texto:
        return "RECIBO"

    # ==========================================
    # REGRA DE NEGÓCIO (FORÇAR FISCAL)
    # ==========================================

    tem_valor = re.search(r'\d+[\.,]\d{2}', texto)
    tem_cnpj = "CNPJ" in texto

    if tem_valor and tem_cnpj:
        return "NFE"

    # ==========================================
    # DECISÃO FINAL
    # ==========================================
    scores = {
        "NFCE": score_nfce,
        "NFE": score_nfe,
        "CTE": score_cte,
        "NFSE": score_nfse
    }

    tipo = max(scores, key=scores.get)

    # mínimo para evitar falso positivo
    if scores[tipo] >= 3:
        return tipo

    return "NAO_FISCAL"