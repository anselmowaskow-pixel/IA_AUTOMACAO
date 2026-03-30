import os
import time
from pathlib import Path
from shutil import copy2

# Configuração das pastas
PASTA_ENTRADA = r"C:\IA_AUTOMACAO\STORAGE\ENTRADA_CLIENTES"
PASTA_SAIDA   = r"C:\IA_AUTOMACAO\STORAGE\PROCESSADOS"

# Cria pastas se não existirem
os.makedirs(PASTA_ENTRADA, exist_ok=True)
os.makedirs(PASTA_SAIDA, exist_ok=True)

# Função simples para "processar" arquivo (pode depois integrar OCR)
def processar_arquivo(caminho_arquivo):
    nome_arquivo = os.path.basename(caminho_arquivo)
    destino = os.path.join(PASTA_SAIDA, nome_arquivo)
    copy2(caminho_arquivo, destino)  # Por enquanto só copia
    print(f"Processado: {nome_arquivo}")

# Monitorando a pasta
print("Monitor de entrada ativo. Aguardando arquivos...")
arquivos_processados = set()

while True:
    arquivos = os.listdir(PASTA_ENTRADA)
    for arq in arquivos:
        caminho = os.path.join(PASTA_ENTRADA, arq)
        if caminho not in arquivos_processados and os.path.isfile(caminho):
            processar_arquivo(caminho)
            arquivos_processados.add(caminho)
    time.sleep(2)  # Espera 2 segundos antes de checar novamente