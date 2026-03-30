# ==========================================================
# ORQUESTRADOR PRO++ - IA_AUTOMACAO
# ==========================================================

import os
import time
import hashlib

from agente_fiscal import analisar_documento
from leitor_qrcode import ler_qrcode
from core_eventos import processar_evento
from interpretador_operacao import interpretar_operacao

BASE_STORAGE = r"C:\IA_AUTOMACAO\STORAGE"
EMPRESAS = {
    "Empresa_A": "46667091004"
}

def gerar_hash(caminho_arquivo):
    try:
        hash_md5 = hashlib.md5()
        with open(caminho_arquivo, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""):
                hash_md5.update(bloco)
        return hash_md5.hexdigest()
    except Exception as e:
        print("ERRO HASH:", e)
        return None


def processar_documento(caminho_arquivo, empresa, doc_empresa):

    arquivo = os.path.basename(caminho_arquivo)

    print("\n-----------------------------")
    print("PROCESSANDO:", arquivo)

    resultado = {
        "arquivo": arquivo,
        "empresa": empresa,
        "status": None,
        "hash": gerar_hash(caminho_arquivo),
        "qr_code": None
    }

    # QR direto (log)
    try:
        qr = ler_qrcode(caminho_arquivo)
        if qr:
            resultado["qr_code"] = qr.get("conteudo")
            print("QR DETECTADO")
    except Exception as e:
        print("ERRO QR:", e)

    # Fiscal
    dados = analisar_documento(caminho_arquivo)

    # Interpretação
    interpretacao = interpretar_operacao(
        entidades=dados,
        doc_empresa=doc_empresa
    )

    # Atualiza resultado
    resultado.update(interpretacao)

    if dados:
        resultado["status"] = dados.get("status")
        resultado["tipo_documento"] = dados.get("tipo")
        resultado["chave_acesso"] = dados.get("chave")

        if dados.get("dados"):
            resultado.update(dados["dados"])

        
    if not resultado.get("status"):
        resultado["status"] = "ERRO"

    print("STATUS FINAL:", resultado["status"])

    return resultado


def processar_todas_empresas():

    for empresa, doc_empresa in EMPRESAS.items():

        pasta = os.path.join(BASE_STORAGE, empresa, "ENTRADA")

        if not os.path.exists(pasta):
            continue

        arquivos = os.listdir(pasta)

        for arquivo in arquivos:

            if not arquivo.lower().endswith((".pdf", ".jpg", ".png")):
                continue

            caminho = os.path.join(pasta, arquivo)

            if not os.path.isfile(caminho):
                continue

            time.sleep(1)
           
            resultado = processar_documento(caminho, empresa, doc_empresa)

            processar_evento(resultado, caminho)

def executar():

    print("🚀 ORQUESTRADOR ATIVO")

    while True:
        try:
            processar_todas_empresas()
        
            
        except Exception as e:
            print("ERRO GERAL:", e)

        time.sleep(5)


if __name__ == "__main__":
    executar()