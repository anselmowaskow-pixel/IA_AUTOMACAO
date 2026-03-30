import os

BASE = r"C:\IA_AUTOMACAO\STORAGE\Empresa_A\AUDITORIA"
ARQUIVO = os.path.join(BASE, "CONTROLE_ID.txt")


def gerar_id():

    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w") as f:
            f.write("0")

    try:
        with open(ARQUIVO, "r") as f:
            ultimo = int(f.read().strip())
    except:
        ultimo = 0

    novo = ultimo + 1

    with open(ARQUIVO, "w") as f:
        f.write(str(novo))

    return f"DOC{novo:06d}"