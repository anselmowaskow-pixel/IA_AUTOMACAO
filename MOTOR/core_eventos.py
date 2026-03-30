# ==========================================================
# CORE EVENTOS PROFISSIONAL - IA_AUTOMACAO
# ==========================================================

import os
import json
import shutil
import csv
from datetime import datetime
from decisor import tomar_decisao, verificar_duplicidade

BASE_STORAGE = r"C:\IA_AUTOMACAO\STORAGE"


# ==========================================================
# DEFINIR DESTINO (GOVERNANÇA)
# ==========================================================

def definir_destino(status):

    if status == "OK":
        return "CONTADOR"

    elif status == "ERRO":
        return "EMPRESA"

    elif status == "ILEGIVEL":
        return "EMPRESA"

    elif status == "DUPLICADO":
        return "ARQUIVO"

    elif status == "NAO_FISCAL":
        return "CONTADOR"

    return "REVISAR"


# ==========================================================
# REGISTRAR EVENTO (CSV)
# ==========================================================

def registrar_evento_csv(resultado):

    empresa = resultado.get("empresa", "SEM_EMPRESA")

    pasta = os.path.join(BASE_STORAGE, empresa, "AUDITORIA")
    os.makedirs(pasta, exist_ok=True)

    caminho_csv = os.path.join(pasta, "EVENTOS_EMPRESA.csv")

    arquivo_existe = os.path.isfile(caminho_csv)

    with open(caminho_csv, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f, delimiter=";")

        if not arquivo_existe:
            writer.writerow([
                "data",
                "hora",
                "empresa",
                "arquivo",
                "tipo_documento",
                "numero_documento",
                "cnpj_emitente",
                "cpf_emitente",
                "natureza_operacao",
                "valor_total",
                "status",
                "acao",
                "destino",
                "observacao",
                "erro",
                "hash"
            ])

        agora = datetime.now()

        writer.writerow([
            agora.strftime("%d/%m/%Y"),
            agora.strftime("%H:%M:%S"),
            resultado.get("empresa"),
            resultado.get("arquivo"),
            resultado.get("tipo_documento"),
            resultado.get("numero_documento"),
            resultado.get("cnpj_emitente"),
            resultado.get("cpf_emitente"),
            resultado.get("natureza_operacao"),
            resultado.get("valor_total"),
            resultado.get("status"),
            resultado.get("acao"),
            resultado.get("destino"),
            resultado.get("observacao"),
            resultado.get("erro"),
            resultado.get("hash")
        ])


# ==========================================================
# SALVAR JSON
# ==========================================================

def salvar_json(resultado):

    empresa = resultado.get("empresa")
    status = resultado.get("status")

    pasta = os.path.join(BASE_STORAGE, empresa, "RESULTADOS", status)
    os.makedirs(pasta, exist_ok=True)

    nome = os.path.splitext(resultado.get("arquivo"))[0]
    caminho = os.path.join(pasta, nome + ".json")

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("✔ JSON SALVO:", caminho)


# ==========================================================
# MOVER ARQUIVO ORIGINAL
# ==========================================================

def mover_arquivo(caminho_arquivo, empresa, status):

    destino = os.path.join(BASE_STORAGE, empresa, "PROCESSADOS")
    os.makedirs(destino, exist_ok=True)

    novo = os.path.join(destino, os.path.basename(caminho_arquivo))

    try:
        shutil.move(caminho_arquivo, novo)
        print("📁 MOVIDO:", novo)
    except Exception as e:
        print("ERRO AO MOVER:", e)


# ==========================================================
# PROCESSAR EVENTO (CÉREBRO)
# ==========================================================

def processar_evento(resultado, caminho_arquivo):

    status = resultado.get("status")

    # =========================
    # REGRA DE NEGÓCIO
    # =========================
    decisao = tomar_decisao(resultado)

    resultado["acao"] = decisao["acao"]
    resultado["observacao"] = decisao["observacao"]
    # =========================
    # DESTINO
    # =========================
    destino = definir_destino(status)
    resultado["destino"] = destino

    # =========================
    # REGISTRAR EVENTO
    # =========================
    registrar_evento_csv(resultado)

    # =========================
    # SALVAR JSON
    # =========================
    salvar_json(resultado)

    # =========================
    # MOVER ARQUIVO
    # =========================
    mover_arquivo(caminho_arquivo, resultado.get("empresa"), status)

    return resultado