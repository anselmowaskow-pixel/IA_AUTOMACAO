# ==========================================================
# DECISOR - IA_AUTOMACAO (REGRA OFICIAL)
# ==========================================================

def verificar_duplicidade(status_atual, chave, hash_doc, base_chaves, base_hashes):

    # ❌ ERRO e ILEGIVEL nunca viram duplicado
    if status_atual in ["ERRO", "ILEGIVEL"]:
        return status_atual

    # ==========================================
    # 🔥 PRIORIDADE 1 — CHAVE DA NF (OFICIAL)
    # ==========================================
    if chave:
        if chave in base_chaves:
            return "DUPLICADO"

    # ==========================================
    # 🔁 FALLBACK — HASH (PDF, imagem, etc)
    # ==========================================
    if hash_doc in base_hashes:
        return "DUPLICADO"

    return status_atual


def decidir_documento(tipo, chave, dados, texto, chave_qr):

    evidencias = []

    # =========================
    # EVIDÊNCIAS
    # =========================

    if chave_qr:
        evidencias.append("QR_VALIDO")

    if chave:
        evidencias.append("CHAVE_TEXTO")

    if tipo in ["NFE", "NFCE"]:
        evidencias.append("TIPO_FISCAL")

    if dados.get("valor"):
        evidencias.append("VALOR_PRESENTE")

    if "DANFE" in texto.upper():
        evidencias.append("PALAVRA_DANFE")

    if "CONSUMIDOR" in texto.upper():
        evidencias.append("PALAVRA_NFCE")

    # =========================
    # SCORE
    # =========================

    score = len(evidencias)

    # =========================
    # DECISÃO
    # =========================

    if "QR_VALIDO" in evidencias:
        return "OK", evidencias

    if "CHAVE_TEXTO" in evidencias and "TIPO_FISCAL" in evidencias:
        return "OK", evidencias

    if score >= 3:
        return "VERIFICAR", evidencias

    return "NAO_FISCAL", evidencias

# ==========================================================
# TOMADA DE DECISÃO
# ==========================================================

def tomar_decisao(resultado):

    status = resultado.get("status")

    if status == "OK":
        return {
            "acao": "LIBERAR",
            "observacao": "Enviar Contador"
        }

    elif status == "ERRO":
        return {
            "acao": "CORRIGIR",
            "observacao": "Enviar Emitente"
        }

    elif status == "ILEGIVEL":
        return {
            "acao": "REENVIAR",
            "observacao": "Enviar Emitente"
        }

    elif status == "NAO_FISCAL":
        return {
            "acao": "ANALISAR",
            "observacao": "Enviar Contador"
        }

    elif status == "DUPLICADO":
        return {
            "acao": "ARQUIVAR",
            "observacao": "Relatar Emitente, Recebedor e Contador"
        }

    # fallback
    return {
        "acao": "ANALISAR",
        "observacao": "Enviar Contador"
    }
