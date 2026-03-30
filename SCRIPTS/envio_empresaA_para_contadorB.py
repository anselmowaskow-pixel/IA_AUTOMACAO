# -*- coding: utf-8 -*-
import os
import time
import shutil

ORIGEM = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\RESULTADOS"
DESTINO = r"C:\IA_AUTOMACAO\STORAGE\Contador B\RECEBIDOS\Empresa A"

os.makedirs(DESTINO, exist_ok=True)
enviados = set()

print("Envio automatico Empresa A -> Contador B ATIVO...")

while True:
    for arquivo in os.listdir(ORIGEM):
        origem_arquivo = os.path.join(ORIGEM, arquivo)
        destino_arquivo = os.path.join(DESTINO, arquivo)

        if origem_arquivo not in enviados and os.path.isfile(origem_arquivo):
            shutil.copy2(origem_arquivo, destino_arquivo)
            enviados.add(origem_arquivo)
            print("ENVIADO:", arquivo)

    time.sleep(2)