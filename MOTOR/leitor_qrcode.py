# ==========================================================
# LEITOR QR CODE PRO+++ - IA_AUTOMACAO
# PyMuPDF + OpenCV | ROBUSTO | MULTI-TENTATIVAS
# ==========================================================

import cv2
import os
import numpy as np
import fitz  # PyMuPDF
import os
os.add_dll_directory(r"C:\IA_AUTOMACAO\libs")

# ==========================================================
# TENTATIVAS DE LEITURA
# ==========================================================
def tentar_qr(detector, img):

    # 1. original
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return data

    # 2. cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data, _, _ = detector.detectAndDecode(gray)
    if data:
        return data

    # 3. threshold (contraste forte)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    data, _, _ = detector.detectAndDecode(thresh)
    if data:
        return data

    # 4. blur leve + threshold
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    data, _, _ = detector.detectAndDecode(thresh2)
    if data:
        return data

    # 5. zoom (QR pequeno)
    zoom = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    data, _, _ = detector.detectAndDecode(zoom)
    if data:
        return data

    # 6. zoom + cinza
    gray_zoom = cv2.cvtColor(zoom, cv2.COLOR_BGR2GRAY)
    data, _, _ = detector.detectAndDecode(gray_zoom)
    if data:
        return data

    return None


# ==========================================================
# LEITOR PRINCIPAL
# ==========================================================
def ler_qrcode(caminho):

    try:
        ext = os.path.splitext(caminho)[1].lower()
        detector = cv2.QRCodeDetector()

        # ======================================
        # IMAGENS
        # ======================================
        if ext in [".jpg", ".jpeg", ".png"]:

            img = cv2.imread(caminho)

            if img is None:
                return None

            resultado = tentar_qr(detector, img)

            if resultado:
                print("QR detectado (imagem)")
                return {"conteudo": resultado}

        # ======================================
        # PDF (ROBUSTO)
        # ======================================
        elif ext == ".pdf":

            doc = fitz.open(caminho)

            for i, pagina in enumerate(doc):

                # resolução alta melhora MUITO QR
                pix = pagina.get_pixmap(dpi=300)

                img = np.frombuffer(pix.samples, dtype=np.uint8)
                img = img.reshape(pix.height, pix.width, pix.n)

                # converter se tiver alpha
                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                resultado = tentar_qr(detector, img)

                if resultado:
                    print(f"QR detectado (PDF página {i})")
                    doc.close()
                    return {"conteudo": resultado}

            doc.close()

        return None

    except Exception as e:
        print("ERRO QR:", e)
        return None