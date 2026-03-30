# ==========================================================
# AGENTE FISCAL PRO++ LIMPO - IA_AUTOMACAO
# ==========================================================

import re
import fitz
import pytesseract
import cv2
import numpy as np

from leitor_qrcode import ler_qrcode


# ==========================================================
# TEXTO PDF DIRETO
# ==========================================================
def extrair_texto_pdf(caminho):
    texto = ""
    try:
        doc = fitz.open(caminho)
        for pagina in doc:
            texto += pagina.get_text()
        doc.close()
    except Exception as e:
        print("ERRO PDF:", e)
    return texto


# ==========================================================
# OCR (IMAGEM)
# ==========================================================
def extrair_texto_ocr(caminho):
    texto = ""
    try:
        doc = fitz.open(caminho)

        for pagina in doc:
            pix = pagina.get_pixmap(dpi=300)
            img = np.frombuffer(pix.samples, dtype=np.uint8)
            img = img.reshape(pix.height, pix.width, pix.n)

            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            texto += pytesseract.image_to_string(gray)

        doc.close()
    except Exception as e:
        print("ERRO OCR:", e)

    return texto


# ==========================================================
# IDENTIFICAR TIPO
# ==========================================================
def identificar_tipo(texto):
    t = texto.upper()

    if "DANFE" in t or "NF-E" in t:
        return "NFE"

    if (
        "CONSUMIDOR" in t
        or "NFC-E" in t
        or "CUPOM FISCAL" in t
        or "DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR" in t
    ):
        return "NFCE"

    return "DESCONHECIDO"


# ==========================================================
# EXTRAIR DADOS
# ==========================================================
def extrair_dados(texto):
    dados = {}

    if not texto:
        return dados

    texto = texto.upper()
    numeros = re.sub(r"\D", "", texto)

    # CHAVE (pega todas e usa a primeira válida)
    chaves = re.findall(r"\d{44}", numeros)
    if chaves:
        dados["chave_acesso"] = chaves[0]

    # CNPJ
    cnpj = re.search(r"\d{14}", numeros)
    if cnpj:
        dados["cnpj_emitente"] = cnpj.group()

    # VALOR
    valores = re.findall(r"\d+[.,]\d{2}", texto)
    if valores:
        dados["valor"] = valores[-1]

    return dados


# ==========================================================
# ESCOLHER MELHOR VALOR
# ==========================================================
def escolher(*args):
    for a in args:
        if a:
            return a
    return None


# ==========================================================
# NOME AMIGÁVEL (PRODUTO)
# ==========================================================
def gerar_nome_amigavel(tipo, dados):
    tipo_str = tipo or "DOC"
    valor = dados.get("valor", "0,00")
    cnpj = dados.get("cnpj_emitente", "")

    nome = f"{tipo_str} - R$ {valor}"

    if cnpj:
        nome += f" ({cnpj})"

    return nome


# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================
def analisar_documento(caminho_arquivo):

    # =========================
    # 1. TEXTO DIRETO
    # =========================
    texto = extrair_texto_pdf(caminho_arquivo)
    print("\n======= TEXTO EXTRAIDO =======\n")
    print(texto[:2000])
    print("\n=============================\n")
    
    # =========================
    # 2. OCR (fallback)
    # =========================
    if len(texto.strip()) < 50:
        texto += extrair_texto_ocr(caminho_arquivo)

    # =========================
    # 3. IDENTIFICAÇÃO
    # =========================
    tipo = identificar_tipo(texto)
    dados = extrair_dados(texto)

    # =========================
    # 4. QR CODE
    # =========================
    chave_qr = None
    qr_code = None

    try:
        qr = ler_qrcode(caminho_arquivo)
        qr_code = qr.get("conteudo") if qr else None

        print("QR RAW:", qr_code)

        if qr_code:

            # 🔹 direto (44 dígitos)
            match = re.search(r"\d{44}", qr_code)
            if match:
                chave_qr = match.group()

            # 🔹 chNFe=
            if not chave_qr:
                match_url = re.search(r"chNFe=(\d{44})", qr_code)
                if match_url:
                    chave_qr = match_url.group(1)

            # 🔹 p= (NFC-e)
            if not chave_qr:
                match_p = re.search(r"p=(\d{44})", qr_code)
                if match_p:
                    chave_qr = match_p.group(1)

    except Exception as e:
        print("ERRO QR:", e)

    # =========================
    # 5. FUSÃO
    # =========================
    chave_final = escolher(
        chave_qr,
        dados.get("chave_acesso")
    )

    # =========================
    # 6. SCORE
    # =========================
    score = 0

    if chave_qr:
        score += 5

    if dados.get("chave_acesso"):
        score += 4

    if tipo in ["NFE", "NFCE"]:
        score += 2

    # =========================
    # DEBUG
    # =========================
    print("------ DEBUG ------")
    print("Tipo:", tipo)
    print("Chave QR:", chave_qr)
    print("Chave Texto:", dados.get("chave_acesso"))
    print("Score:", score)
    print("-------------------")

    # =========================
    # NOME AMIGÁVEL
    # =========================
    nome_amigavel = gerar_nome_amigavel(tipo, dados)

    # =========================
    # RESULTADO FINAL
    # =========================
    if score >= 4:
        status = "OK"
    elif score >= 2:
        status = "VERIFICAR"
    else:
        status = "NAO_FISCAL"

    return {
        "status": status,
        "tipo": tipo if tipo != "DESCONHECIDO" else "NFCE",
        "chave": chave_final,
        "dados": dados,
        "qr_code": qr_code,
        "nome_amigavel": nome_amigavel,
        "confianca": score
    }