# ==========================================
# CLASSIFICADOR DE EVENTO ECONÔMICO
# IA_AUTOMACAO
# ==========================================

def classificar_evento(tipo_documento, texto):

    texto = (texto or "").upper()

    evento = {
        "categoria_evento": "ADMINISTRATIVO",
        "impacto_fiscal": False,
        "impacto_financeiro": False
    }

    # ======================================
    # DOCUMENTOS FISCAIS
    # ======================================

    if tipo_documento in ["NFE", "NFCE", "CTE", "SAT", "CFE"]:

        evento["categoria_evento"] = "FISCAL"
        evento["impacto_fiscal"] = True
        evento["impacto_financeiro"] = True

        return evento

    # ======================================
    # BOLETO
    # ======================================

    if tipo_documento == "BOLETO":

        evento["categoria_evento"] = "FINANCEIRO"
        evento["impacto_financeiro"] = True

        return evento

    # ======================================
    # RECIBO
    # ======================================

    if tipo_documento == "RECIBO":

        evento["categoria_evento"] = "DESPESA"
        evento["impacto_financeiro"] = True

        return evento

    # ======================================
    # CONTA DE ENERGIA
    # ======================================

    if "ENERGIA" in texto or "KWH" in texto:

        evento["categoria_evento"] = "CUSTO"
        evento["impacto_fiscal"] = True
        evento["impacto_financeiro"] = True

        return evento

    return evento