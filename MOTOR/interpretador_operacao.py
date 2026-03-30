# ==========================================================
# INTERPRETADOR DE OPERAÇÃO - IA_AUTOMACAO
# ==========================================================

# =========================
# FUNÇÃO PADRÃO DESCRIÇÃO
# =========================
def gerar_descricao(categoria, nome_emitente=None, valor=None):

    if not categoria:
        categoria = "OUTROS"

    categoria = categoria.upper()
    nome_emitente = nome_emitente or "Documento"

    mapa = {
        "COMBUSTIVEL": "Combustível",
        "INSUMO": "Insumo",
        "CONSUMO": "Consumo",
        "TRANSPORTE": "Frete",
        "SERVICO": "Serviço",
        "VENDA": "Venda",
        "OUTROS": "Movimento"
    }

    categoria_legivel = mapa.get(categoria, categoria.title())

    if valor:
        try:
            valor_formatado = f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return f"{categoria_legivel} - {nome_emitente} - R$ {valor_formatado}"
        except:
            return f"{categoria_legivel} - {nome_emitente} - R$ {valor}"

    return f"{categoria_legivel} - {nome_emitente}"


def limpar_nome_emitente(nome):

    if not nome:
        return "Documento"

    nome = nome.upper().strip()

    # =========================
    # REMOVER LIXO COMUM OCR
    # =========================
    lixo = [
        "LTDA", "LTD", "EIRELI", "EPP", "ME",
        "S/A", "SA", "DA", "DE", "DO", "DOS", "DAS"
    ]

    palavras = nome.split()
    palavras_filtradas = [p for p in palavras if p not in lixo]

    nome = " ".join(palavras_filtradas)

    # =========================
    # CORREÇÕES INTELIGENTES
    # =========================
    substituicoes = {
        "POSTO DE COMBUSTIVEL": "Posto",
        "AUTO POSTO": "Posto",
        "POSTO": "Posto",
        "SUPERMERCADO": "Supermercado",
        "MERCADO": "Mercado",
        "TRANSPORTES": "Transportadora",
        "TRANSPORTE": "Transportadora",
        "LOGISTICA": "Transportadora"
    }

    for chave, valor in substituicoes.items():
        if chave in nome:
            return valor

    # =========================
    # PADRÃO FINAL (TÍTULO)
    # =========================
    return nome.title()

# =========================
# FUNÇÃO PRINCIPAL
# =========================
def interpretar_operacao(entidades, doc_empresa=None):

    # =========================
    # PROTEÇÃO
    # =========================
    if not entidades:
        return {
            "tipo_movimento": "OUTROS",
            "direcao": "DESCONHECIDO",
            "categoria": "OUTROS",
            "descricao": "Sem dados",
            "confianca": 0
        }

    # =========================
    # FUNÇÃO AUXILIAR
    # =========================
    def limpar_doc(doc):
        return "".join(filter(str.isdigit, doc)) if doc else None

    def doc_igual(doc1, doc2):
        return doc1 and doc2 and doc1 == doc2

    # =========================
    # EXTRAÇÃO DE DADOS
    # =========================
    cnpj_emitente = limpar_doc(entidades.get("cnpj_emitente"))
    cnpj_destinatario = limpar_doc(entidades.get("cnpj_destinatario"))
    cpf_emitente = limpar_doc(entidades.get("cpf_emitente"))
    cpf_destinatario = limpar_doc(entidades.get("cpf_destinatario"))

    tipo_documento = entidades.get("tipo_documento")
    texto = (entidades.get("texto") or "").upper()
    valor = entidades.get("valor")
    nome_emitente = entidades.get("nome_emitente")

    doc_empresa = limpar_doc(doc_empresa)

    # =========================
    # DIREÇÃO (ENTRADA / SAIDA)
    # =========================
    direcao = "DESCONHECIDO"

    if doc_empresa:
        if doc_igual(doc_empresa, cnpj_destinatario) or doc_igual(doc_empresa, cpf_destinatario):
            direcao = "ENTRADA"
        elif doc_igual(doc_empresa, cnpj_emitente) or doc_igual(doc_empresa, cpf_emitente):
            direcao = "SAIDA"

    # =========================
    # CLASSIFICAÇÃO BASE
    # =========================
    categoria = "OUTROS"
    confianca = 0.5

    # =========================
    # REGRAS DE NEGÓCIO
    # =========================

    # NFC-e
    if tipo_documento == "NFCE":
        categoria = "CONSUMO"
        direcao = "ENTRADA"
        confianca = 0.85

    # Combustível
    elif any(p in texto for p in ["POSTO", "COMBUSTIVEL", "GASOLINA", "DIESEL"]):
        categoria = "COMBUSTIVEL"
        confianca = 0.9

    # Insumo agrícola
    elif any(p in texto for p in ["UREIA", "FERTILIZANTE", "ADUBO"]):
        categoria = "INSUMO"
        confianca = 0.95

    # Supermercado
    elif "SUPERMERCADO" in texto:
        categoria = "CONSUMO"
        confianca = 0.8

    # Transporte
    elif tipo_documento == "CTE" or any(p in texto for p in ["FRETE", "TRANSPORTE"]):
        categoria = "TRANSPORTE"
        confianca = 0.9
        direcao = "ENTRADA"   # 🔥 IMPORTANTE

    # Serviço
    elif "SERVICO" in texto or "SERVIÇ" in texto:
        categoria = "SERVICO"
        confianca = 0.8

    # =========================
    # FALLBACK NFE (INTELIGENTE)
    # =========================
    if direcao == "DESCONHECIDO" and tipo_documento == "NFE":

        # Se não sou o emitente → provavelmente comprei
        if not doc_igual(doc_empresa, cnpj_emitente):
            direcao = "ENTRADA"
            confianca += 0.2

    # =========================
    # TIPO DE MOVIMENTO
    # =========================
    if direcao == "ENTRADA":
        if categoria in ["COMBUSTIVEL", "CONSUMO", "SERVICO", "TRANSPORTE"]:
            tipo_movimento = "DESPESA"
        else:
            tipo_movimento = "ENTRADA"

    elif direcao == "SAIDA":
        tipo_movimento = "RECEITA"

    else:
        tipo_movimento = "OUTROS"

    # =========================
    # AJUSTE DE CONFIANÇA
    # =========================
    if direcao != "DESCONHECIDO":
        confianca += 0.1

    # =========================
    # DESCRIÇÃO FINAL
    # =========================
    descricao = gerar_descricao(categoria, nome_emitente, valor)

    # =========================
    # RESULTADO FINAL
    # =========================
    return {
        "tipo_movimento": tipo_movimento,
        "direcao": direcao,
        "categoria": categoria,
        "descricao": descricao,
        "confianca": round(confianca, 2)
    }