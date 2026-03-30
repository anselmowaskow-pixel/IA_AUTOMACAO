import os
import shutil

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa_TESTE"

ENTRADA = os.path.join(BASE, "ENTRADA")
PROCESSADOS = os.path.join(BASE, "PROCESSADOS")

def processar():
    arquivos = os.listdir(ENTRADA)

    for arquivo in arquivos:
        origem = os.path.join(ENTRADA, arquivo)
        destino = os.path.join(PROCESSADOS, arquivo)

        if os.path.isfile(origem):
            print(f"Processando: {arquivo}")
            shutil.move(origem, destino)

if __name__ == "__main__":
    processar()