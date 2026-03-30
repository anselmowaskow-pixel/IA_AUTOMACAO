def interpretar_intencao(evento):

    status = evento.get("status", "").upper()
    operacao = evento.get("operacao", "").upper()
    documento = evento.get("documento", "")

    if status == "OK" and operacao == "COMPRA":
        return "REGISTRAR_COMPRA"

    if status == "OK" and operacao == "VENDA":
        return "REGISTRAR_VENDA"

    if status == "ILEGIVEL":
        return "SOLICITAR_REENVIO"

    if status == "DUPLICADO":
        return "IGNORAR_DOCUMENTO"

    if status == "NAO_FISCAL":
        return "ARQUIVAR_DOCUMENTO"

    return "VERIFICAR_MANUAL"