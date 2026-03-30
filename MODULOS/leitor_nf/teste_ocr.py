import os
import re
import cv2
import pytesseract
from datetime import datetime

# ===============================
# CONFIGURACOES FIXAS
# ===============================

TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_DIR = r"C:\TESSDATA"
IMAGEM_TESTE = "teste.jpg"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR

# ===============================
# FUNCOES AUXILIARES
# ===============================

def limpar_numero(txt):
    if not txt:
        return None
    return re.sub(r"\D", "", txt)

def extrair_primeiro(padrao, texto):
    achado = re.search(padrao, texto, re.MULTILINE)
    return achado.group(1).strip() if achado else None

# ===============================
# OCR COM RUIDO CONTROLADO
# ===============================

def rodar_ocr(imagem_path):
    if not os.path.exists(imagem_path):
        raise FileNotFoundError("Imagem nao encontrada: " + imagem_path)

    img = cv2.imread(imagem_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        8
    )

    cv2.imwrite("teste_tratada.png", thresh)

    texto = pytesseract.image_to_string(
        thresh,
        lang="por",
        config="--oem 3 --psm 4"
    )

    return texto

# ===============================
# EXTRATOR CANONICO DE NF
# ===============================

def extrair_nf(texto):
    nf = {
        "tipo_documento": "NF-e",
        "chave_acesso": None,
        "numero_nf": None,
        "serie": None,
        "data_emissao": None,
        "emitente": {
            "cnpj": None,
            "razao_social": None
        },
        "destinatario": {
            "cpf_cnpj": None,
            "nome": None
        },
        "valor_total_nf": None,
        "status_leitura": "OCR_OK",
        "raw_ocr": texto
    }

    # CHAVE DE ACESSO (44 DIGITOS)
    chaves = re.findall(r"\b\d{44}\b", texto)
    if chaves:
        nf["chave_acesso"] = chaves[0]

    # NUMERO DA NF
    nf["numero_nf"] = extrair_primeiro(
        r"N[ºo]\s*0*([0-9]{3,})",
        texto
    )

    # SERIE
    nf["serie"] = extrair_primeiro(
        r"S[EÉ]RIE\s*0*([0-9]+)",
        texto
    )

    # DATA EMISSAO
    datas = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texto)
    if datas:
        nf["data_emissao"] = datas[0]

    # CNPJ EMITENTE
    cnpjs = re.findall(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b", texto)
    if cnpjs:
        nf["emitente"]["cnpj"] = limpar_numero(cnpjs[0])

    # CPF OU CNPJ DESTINATARIO
    cpfs = re.findall(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", texto)
    if cpfs:
        nf["destinatario"]["cpf_cnpj"] = limpar_numero(cpfs[0])

    # RAZAO SOCIAL EMITENTE (HEURISTICA)
    razao = extrair_primeiro(
        r"IDENTIFICAÇÃO DO EMITENTE\s+([A-Z0-9\.\s]{5,})",
        texto
    )
    if razao:
        nf["emitente"]["razao_social"] = razao

    # NOME DESTINATARIO (HEURISTICA)
    nome = extrair_primeiro(
        r"DESTINAT[AÁ]RIO\s*/\s*REMETENTE\s+([A-Z\s]{5,})",
        texto
    )
    if nome:
        nf["destinatario"]["nome"] = nome

    # CLASSIFICACAO FINAL
    if not nf["chave_acesso"]:
        nf["status_leitura"] = "ILEGIVEL"
    elif not nf["emitente"]["cnpj"]:
        nf["status_leitura"] = "INCOMPLETA"

    return nf

# ===============================
# EXECUCAO PRINCIPAL
# ===============================

if __name__ == "__main__":
    print("=== INICIO OCR NF ===")

    texto_ocr = rodar_ocr(IMAGEM_TESTE)

    print("=== TEXTO OCR ===")
    print(texto_ocr)

    dados_nf = extrair_nf(texto_ocr)

    print("\n=== JSON CANONICO GERADO ===")
    print(dados_nf)

    print("\n=== FIM ===")