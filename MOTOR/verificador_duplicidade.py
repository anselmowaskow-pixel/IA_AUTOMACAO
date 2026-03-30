import hashlib
import os

ARQUIVO_HASHES = r"C:\IA_AUTOMACAO\STORAGE\Empresa_A\AUDITORIA\HASHES_PROCESSADOS.txt"


def calcular_hash(caminho):

    hash_md5 = hashlib.md5()

    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloco)

    return hash_md5.hexdigest()


def verificar_duplicidade(caminho):

    hash_arquivo = calcular_hash(caminho)

    if not os.path.exists(ARQUIVO_HASHES):
        open(ARQUIVO_HASHES, "w").close()

    with open(ARQUIVO_HASHES, "r") as f:
        hashes = f.read().splitlines()

    if hash_arquivo in hashes:
        return True

    with open(ARQUIVO_HASHES, "a") as f:
        f.write(hash_arquivo + "\n")

    return False