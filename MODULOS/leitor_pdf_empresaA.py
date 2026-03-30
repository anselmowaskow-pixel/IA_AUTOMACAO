import os
import time
from pdfminer.high_level import extract_text

PASTA_ENTRADA = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\PASTA_ENTRADA"
PASTA_RESULTADOS = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\RESULTADOS"
PASTA_PROCESSADOS = r"C:\IA_AUTOMACAO\STORAGE\Empresa A\PROCESSADOS"

print("LEITOR PDF ATIVO - Empresa A")

while True:
    for arq in os.listdir(PASTA_ENTRADA):
        if arq.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(PASTA_ENTRADA, arq)

            try:
                texto = extract_text(caminho_pdf)

                nome_base = arq.replace(".pdf", "")
                saida_txt = os.path.join(PASTA_RESULTADOS, nome_base + ".txt")

                with open(saida_txt, "w", encoding="utf-8") as f:
                    f.write(texto)

                os.rename(
                    caminho_pdf,
                    os.path.join(PASTA_PROCESSADOS, arq)
                )

                print(f"[OK] PDF processado -> {nome_base}")

            except Exception as e:
                print(f"[ERRO] {arq}: {e}")

    time.sleep(2)