# ======================================================
# MODELO CANÔNICO DE EVENTO ECONÔMICO
# IA_AUTOMACAO
# ======================================================

import uuid
import datetime


def criar_evento(documento):

    evento = {

        "id_evento": str(uuid.uuid4()),

        "empresa": documento.get("empresa"),

        "arquivo": documento.get("arquivo"),

        "tipo_evento": documento.get("tipo_evento", "DOCUMENTO"),

        "documento": documento.get("documento"),

        "numero": documento.get("numero"),

        "valor": documento.get("valor"),

        "natureza_operacao": documento.get("nat_operacao"),

        "status": documento.get("status"),

        "acao": None,

        "timestamp": datetime.datetime.now().isoformat()

    }

    return evento