import re


def extrair_dados_fiscais(texto):

    # ===============================
    # NORMALIZAÇÃO DO TEXTO
    # ===============================

    texto = texto.upper()
    texto = texto.replace("\n", " ")
    texto = texto.replace("\r", " ")
    texto = re.sub(r"\s+", " ", texto)

    dados = {
        "documento": "desconhecido",
        "numero": None,
        "serie": None,
        "cnpj_emitente": None,
        "cpf_emitente": None,
        "cpf_destinatario": None,
        "cnpj_destinatario": None,
        "emitente": None,
        "produto": None,
        "quantidade": None,
        "valor": None,
        "pagamento": None,
        "data": None,
        "hora": None,
        "cidade": None,
        "chave_acesso": None,
        "confianca": "baixa"
    }

    # ===============================
    # DETECTAR TIPO DOCUMENTO (ROBUSTO)
    # ===============================

    if any(p in texto for p in [
        "NFC-E",
        "NFCE",
        "CONSUMIDOR ELETRONICA",
        "CONSUMIDOR ELETRÔNICA",
        "DOCUMENTO AUXILIAR DA NOTA",
        "NOTA FISCAL DE CONSUMIDOR",
    ]):
        dados["documento"] = "NFCe"

    elif any(p in texto for p in [
        "DANFE",
        "NOTA FISCAL ELETRONICA",
        "NOTA FISCAL ELETRÔNICA",
        "CHAVE DE ACESSO",
    ]):
        dados["documento"] = "NFe"

    elif any(p in texto for p in [
        "NOTA FISCAL DE SERVICO",
        "NOTA FISCAL DE SERVIÇO",
        "NFS-E",
    ]):
        dados["documento"] = "NFSe"
    
    # ===============================
    # CNPJ EMITENTE (MELHORADO)
    # ===============================

    # tenta pegar bloco do emitente
    bloco_emit = None

    match_emit = re.search(r"(EMITENTE|FORNECEDOR).*?(?=DESTINAT|DANFE|$)", texto)

    if match_emit:
        bloco_emit = match_emit.group()
    else:
        bloco_emit = texto[:500]  # fallback início do documento

    cnpj_emit = re.search(r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}", bloco_emit)

    if cnpj_emit:
        dados["cnpj_emitente"] = re.sub(r"\D", "", cnpj_emit.group())

    # ===============================
    # CPF
    # ===============================
    # ===============================
    # CPF / CNPJ DESTINATÁRIO (NOVO)
    # ===============================

    # tenta pegar bloco do destinatário
    bloco_dest = None

    match = re.search(r"DESTINAT[ÁA]RIO.*?(?=TOTAL|VALOR|DANFE|$)", texto)

    if match:
        bloco_dest = match.group()
    else:
        bloco_dest = texto  # fallback

    # CPF destinatário
    cpf_dest = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", bloco_dest)
    if cpf_dest:
        dados["cpf_destinatario"] = re.sub(r"\D", "", cpf_dest.group())

    # CNPJ destinatário
    cnpj_dest = re.search(r"\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}", bloco_dest)
    if cnpj_dest:
        dados["cnpj_destinatario"] = re.sub(r"\D", "", cnpj_dest.group())

    # ===============================
    # NFC-e → consumidor padrão
    # ===============================
    if dados["documento"] == "NFCe" and not dados["cpf_destinatario"] and not dados["cnpj_destinatario"]:
        dados["cpf_destinatario"] = "CONSUMIDOR"

    # ===============================
    # NUMERO DA NOTA
    # ===============================

    numero = re.search(r"NFC.?E.*?(\d{3,9})", texto)

    if numero:
        dados["numero"] = numero.group(1)

    # ===============================
    # SERIE
    # ===============================

    serie = re.search(r"S[ÉE]RIE\s*(\d+)", texto)

    if serie:
        dados["serie"] = serie.group(1)

    # ===============================
    # VALOR
    # ===============================

    valor = re.search(r"(VALOR TOTAL|VALOR PAGO)[^\d]*(\d+[\.,]\d{2})",                     texto)

    if valor:
        dados["valor"] = valor.group(2)
        

    # ===============================
    # PRODUTO
    # ===============================

    produto = re.search(
        r"(DIESEL\s*S?-?500|DIESEL\s*S?-?10|DIESEL|GASOLINA|ETANOL)",
        texto
    )

    if produto:
        dados["produto"] = produto.group(1)

    # ===============================
    # QUANTIDADE
    # ===============================

    qtd = re.search(r"(\d+[\.,]\d+)\s*(L|LT|LITRO|UN)", texto)

    if qtd:
        dados["quantidade"] = qtd.group(1)

    # ===============================
    # PAGAMENTO
    # ===============================

    pagamento = re.search(
        r"(PIX|DINHEIRO|CARTAO|CARTÃO|DEBITO|CR[ÉE]DITO|BOLETO)",
        texto
    )

    if pagamento:
        dados["pagamento"] = pagamento.group(1)

    # ===============================
    # DATA E HORA
    # ===============================

    datahora = re.search(r"(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})", texto)

    if datahora:
        dados["data"] = datahora.group(1)
        dados["hora"] = datahora.group(2)

    # ===============================
    # CIDADE (REGIÃO SUL EXEMPLO)
    # ===============================

    cidade = re.search(r"(CANGUCU|CANGUÇU|PELOTAS|RIO GRANDE)", texto)

    if cidade:
        dados["cidade"] = cidade.group(1)

    # ===============================
    # CHAVE DE ACESSO (NFE)
    # ===============================

    texto_numeros = re.sub(r"\D", "", texto)
    chave = re.search(r"\d{44}", texto_numeros)


    if chave:
        chave_limpa = chave.group()

        dados["chave_acesso"] = chave_limpa
        dados["numero"] = chave_limpa  # 🔥 ESSENCIAL

    # ===============================
    # CONFIANÇA DA EXTRAÇÃO
    # ===============================

    if dados["valor"] and dados["cnpj_emitente"]:
        dados["confianca"] = "alta"

    return dados


# =====================================
# FUNÇÕES COMPATÍVEIS COM AGENTE_FISCAL
# =====================================

def extrair_cnpj(texto):

    dados = extrair_dados_fiscais(texto)

    return dados.get("cnpj_emitente")


def extrair_valor(texto):

    dados = extrair_dados_fiscais(texto)

    return dados.get("valor")


def extrair_cpf(texto):

    dados = extrair_dados_fiscais(texto)

    return dados.get("cpf")