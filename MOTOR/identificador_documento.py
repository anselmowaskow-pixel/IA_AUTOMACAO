def identificar_documento(entidades):

    texto = entidades.get("texto", "")
    qr = entidades.get("qr_code", "")

    if texto:
        texto = texto.upper()

    if qr:
        qr = qr.lower()

    # ==========================================
    # NFC-e (cupom fiscal)
    # ==========================================
    if any(p in texto for p in [
        "NFC-E",
        "NFCE",
        "CONSUMIDOR ELETRONICA",
        "CONSUMIDOR ELETRÔNICA",
        "DOCUMENTO AUXILIAR DA NOTA",
        "NOTA FISCAL DE CONSUMIDOR"
    ]):
        return "NFCE"

    # ==========================================
    # NF-e (DANFE)
    # ==========================================
    if any(p in texto for p in [
        "DANFE",
        "NOTA FISCAL ELETRONICA",
        "NOTA FISCAL ELETRÔNICA",
        "CHAVE DE ACESSO"
    ]):
        return "NFE"

    # ==========================================
    # CT-e
    # ==========================================
    if any(p in texto for p in [
        "CONHECIMENTO DE TRANSPORTE",
        "CT-E",
        "DACTE"
    ]):
        return "CTE"

    # ==========================================
    # NFSe
    # ==========================================
    if any(p in texto for p in [
        "NOTA FISCAL DE SERVICO",
        "NOTA FISCAL DE SERVIÇO",
        "NFS-E",
        "NFSE"
    ]):
        return "NFSE"

    # ==========================================
    # RECIBO FRETE
    # ==========================================
    if any(p in texto for p in [
        "RECIBO DE FRETE",
        "CIOT"
    ]):
        return "RECIBO_FRETE"

    # ==========================================
    # QR Code fiscal
    # ==========================================
    if qr:
        if "nfe.fazenda.gov.br" in qr:
            return "NFE"

        if "nfce.fazenda" in qr:
            return "NFCE"

    # ==========================================
    # HEURÍSTICA EXTRA (MUITO FORTE)
    # ==========================================
    if "SEFAZ" in texto and "CHAVE" in texto:
        return "NFCE"

    # ==========================================
    # PADRÃO
    # ==========================================
    return "NAO_FISCAL"