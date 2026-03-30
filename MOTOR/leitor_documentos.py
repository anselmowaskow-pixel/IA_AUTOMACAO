import fitz
import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def ler_pymupdf(caminho):
    try:
        texto = ""
        doc = fitz.open(caminho)
        for p in doc:
            texto += p.get_text()
        return texto.strip()
    except:
        return ""


def ler_pdfplumber(caminho):
    try:
        texto = ""
        with pdfplumber.open(caminho) as pdf:
            for p in pdf.pages:
                texto += p.extract_text() or ""
        return texto.strip()
    except:
        return ""


def ler_ocr(caminho):
    try:
        texto = ""
        imagens = convert_from_path(caminho)
        for img in imagens:
            texto += pytesseract.image_to_string(img, lang="por")
        return texto.strip()
    except:
        return ""


def ler_documento(caminho):

    # 1️⃣ PyMuPDF (rápido)
    texto = ler_pymupdf(caminho)
    if len(texto) > 80:
        print("✔ PyMuPDF")
        return texto

    # 2️⃣ pdfplumber (mais profundo)
    texto = ler_pdfplumber(caminho)
    if len(texto) > 80:
        print("✔ pdfplumber")
        return texto

    # 3️⃣ OCR (pesado)
    print("⚠ OCR ativado")
    return ler_ocr(caminho)