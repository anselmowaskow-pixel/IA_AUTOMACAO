import os
import csv

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa_A\AUDITORIA"

EVENTOS = os.path.join(BASE, "EVENTOS_EMPRESA.csv")
DECISOES = os.path.join(BASE, "DECISOES_EMPRESA.csv")


def definir_acao(status):

    if status == "OK":
        return "LIBERAR"

    if status == "NAO_FISCAL":
        return "ARQUIVAR"

    if status == "ILEGIVEL":
        return "ANALISAR"

    if status == "ERRO":
        return "VERIFICAR"

    if status == "DUPLICADO":
        return "IGNORAR"

    return "ARQUIVAR"


def gerar_decisoes():

    linhas = []

    with open(EVENTOS, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f, delimiter=";")

        for row in reader:

            data = row.get("data","")
            hora = row.get("hora","")
            documento = row.get("arquivo","")
            operacao = row.get("nat_operacao","")
            status = (row.get("status") or "").upper().strip()

            if not documento:
                continue

            acao = definir_acao(status)

            linhas.append({
                "data": data,
                "hora": hora,
                "documento": documento,
                "operacao": operacao,
                "status": status,
                "acao": acao,
                "arquivo": documento
            })

    with open(DECISOES, "w", newline="", encoding="utf-8") as f:

        campos = [
            "data",
            "hora",
            "documento",
            "operacao",
            "status",
            "acao",
            "arquivo"
        ]

        writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(linhas)

    print("DECISOES atualizadas:", len(linhas))


if __name__ == "__main__":
    gerar_decisoes()