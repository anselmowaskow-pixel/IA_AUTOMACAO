import os
import re
import hashlib
from datetime import datetime

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

# =========================
# CONFIGURAÇÕES
# =========================

# AJUSTE SEU CAMINHO DO TESSERACT
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================
# OCR / EXTRAÇÃO DE TEXTO
# =========================

def extrair_texto_pdf(caminho_pdf):
    texto = ""

    # 1) Tenta texto direto (PDF digital)
    try:
        reader = PdfReader(caminho_pdf)
        for page in reader.pages:
            texto += page.extract_text() or ""
    except Exception:
        pass

    # 2) Se não achou texto suficiente, faz OCR
    if len(texto.strip()) < 50:
        imagens = convert_from_path(caminho_pdf, dpi=300)
        for img in imagens:
            texto += pytesseract.image_to_string(img, lang="por")

    return texto.upper()

# =========================
# CLASSIFICADOR
# =========================

def classificar_documento(texto):
    classe = "OUTRO"
    subtipo = ""
    observacao = ""

    # NF-e / DANFE
    if "DANFE" in texto and re.search(r"\d{44}", texto):
        classe = "NF_E"
        observacao = "Nota Fiscal Eletrônica identificada"

    # Cupom Fiscal
    elif "CUPOM FISCAL" in texto or "SAT" in texto or "NFC-E" in texto:
        classe = "CUPOM_FISCAL"
        observacao = "Cupom fiscal identificado"

    # PIX
    elif "PIX" in texto or "QR CODE" in texto and "BANCO" in texto:
        classe = "COMPROVANTE_PAGAMENTO"
        subtipo = "PIX"
        observacao = "Comprovante de pagamento PIX"

    # Energia
    elif "ENERGIA" in texto or "KWH" in texto or "DISTRIBUIDORA" in texto:
        classe = "CONTA_SERVICO"
        subtipo = "ENERGIA"
        observacao = "Conta de energia elétrica"

    # Internet / telefone
    elif "INTERNET" in texto or "TELEFONE" in texto or "FIBRA" in texto:
        classe = "CONTA_SERVICO"
        subtipo = "TELECOM"
        observacao = "Conta de serviço de telecomunicação"

    # Recibo
    elif "RECIBO" in texto:
        classe = "RECIBO"
        observacao = "Recibo identificado"

    return classe, subtipo, observacao

# =========================
# EXTRAÇÕES IMPORTANTES
# =========================

def extrair_data(texto):
    padrao = r"(\d{2}/\d{2}/\d{4})"
    match = re.search(padrao, texto)
    return match.group(1) if match else ""

def extrair_cnpj(texto):
    padrao = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
    match = re.search(padrao, texto)
    return match.group(0) if match else ""

# =========================
# AGENTE PRINCIPAL
# =========================

def analisar_documento(caminho_pdf):
    texto = extrair_texto_pdf(caminho_pdf)

    classe, subtipo, obs = classificar_documento(texto)

    data_doc = extrair_data(texto)
    cnpj = extrair_cnpj(texto)

    status = "OK"
    if classe == "NF_E" and not re.search(r"\d{44}", texto):
        status = "ATENCAO"
        obs = "NF-e sem chave completa"

    resultado = {
        "arquivo": os.path.basename(caminho_pdf),
        "classe_documento": classe,
        "subtipo": subtipo,
        "cnpj_emitente": cnpj,
        "data_documento": data_doc,
        "data_evento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "observacao": obs
    }

    return resultado

# =========================
# TESTE DIRETO
# =========================

if __name__ == "__main__":
    pdf = r"C:\TESTE\documento.pdf"
    resultado = analisar_documento(pdf)
    for k, v in resultado.items():
        print(f"{k}: {v}")