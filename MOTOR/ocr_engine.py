# ==========================================================
# OCR ENGINE LIMPO - IA_AUTOMACAO (VERSÃO FINAL)
# ==========================================================

import fitz
import pdfplumber
import pytesseract

from PIL import Image
import io


# ==========================================
# TEXTO DIRETO (PDF DIGITAL)
# ==========================================

def extrair_texto_pdf(caminho):

    texto_total = ""

    try:
        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_total += texto + "\n"

    except Exception as e:
        print(f"ERRO PDFPLUMBER: {e}")

    return texto_total


# ==========================================
# OCR (PDF ESCANEADO)
# ==========================================

def extrair_texto_ocr(caminho):

    texto_total = ""

    try:
        doc = fitz.open(caminho)

        for page in doc:
            try:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")

                img = Image.open(io.BytesIO(img_bytes))

                texto = pytesseract.image_to_string(img, lang="por")

                if texto:
                    texto_total += texto + "\n"

            except Exception as e:
                print(f"ERRO PAGINA OCR: {e}")

    except Exception as e:
        print(f"ERRO OCR GERAL: {e}")

    return texto_total


# ==========================================
# LEITOR INTELIGENTE (OFICIAL)
# ==========================================

def ler_pdf(caminho):

    # 1. tenta texto direto
    texto = extrair_texto_pdf(caminho)

    if texto and len(texto.strip()) > 30:
        print("📄 PDF TEXTO DETECTADO")
        return texto

    # 2. fallback OCR
    print("🧠 OCR ATIVADO")

    texto = extrair_texto_ocr(caminho)

    if not texto or not texto.strip():
        print("❌ PDF ILEGÍVEL")
        return None

    return texto