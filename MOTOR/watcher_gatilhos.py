# -*- coding: utf-8 -*-
import os
import time
import subprocess
from datetime import datetime

# =========================
# CONFIGURAÇÃO CANÔNICA
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "..", "STORAGE")
GATILHOS_DIR = os.path.join(STORAGE_DIR, "Empresa_A", "GATILHOS")

ORQUESTRADOR_CMD = ["python", os.path.join(BASE_DIR, "orquestrador.py")]

GATILHOS_VALIDOS = {"APROVAR", "REJEITAR", "REPROCESSAR"}

INTERVALO_SEGUNDOS = 2


# =========================
# FUNÇÕES
# =========================

def log(msg):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[WATCHER {agora}] {msg}", flush=True)


def executar_orquestrador():
    log("Chamando orquestrador...")
    subprocess.Popen(ORQUESTRADOR_CMD, cwd=BASE_DIR)


def consumir_gatilho(nome_arquivo):
    caminho = os.path.join(GATILHOS_DIR, nome_arquivo)

    if not os.path.isfile(caminho):
        return

    if nome_arquivo not in GATILHOS_VALIDOS:
        log(f"Gatilho ignorado: {nome_arquivo}")
        return

    log(f"GATILHO DETECTADO -> {nome_arquivo}")
    executar_orquestrador()

    try:
        os.remove(caminho)
        log(f"Gatilho consumido -> {nome_arquivo}")
    except Exception as e:
        log(f"ERRO ao remover gatilho: {e}")


# =========================
# LOOP PRINCIPAL
# =========================

def main():
    log("GATILHOS ATIVOS — EXECUÇÃO CONTROLADA")

    if not os.path.exists(GATILHOS_DIR):
        os.makedirs(GATILHOS_DIR)

    while True:
        try:
            arquivos = os.listdir(GATILHOS_DIR)
            for nome in arquivos:
                consumir_gatilho(nome)

            time.sleep(INTERVALO_SEGUNDOS)

        except KeyboardInterrupt:
            log("WATCHER FINALIZADO PELO USUÁRIO")
            break
        except Exception as e:
            log(f"ERRO GERAL: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()