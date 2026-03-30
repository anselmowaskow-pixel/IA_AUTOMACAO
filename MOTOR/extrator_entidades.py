# ==========================================
# EXTRATOR DE ENTIDADES
# IA_AUTOMACAO
# ==========================================

import re


def extrair_entidades(texto):

    texto = texto or ""

    resultado = {
        "cnpj": None,
        "cpf": None,
        "valor": None,
        "data": None
    }

    # ======================================
    # CNPJ
    # ======================================

    cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)

    if cnpj:
        resultado["cnpj"] = cnpj.group()

    # ======================================
    # CPF
    # ======================================

    cpf = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)

    if cpf:
        resultado["cpf"] = cpf.group()

    # ======================================
    # VALOR
    # ======================================

    valor = re.search(r"R\$\s?\d+[.,]\d{2}", texto)

    if valor:
        resultado["valor"] = valor.group()

    # ======================================
    # DATA
    # ======================================

    data = re.search(r"\d{2}/\d{2}/\d{4}", texto)

    if data:
        resultado["data"] = data.group()

    return resultado