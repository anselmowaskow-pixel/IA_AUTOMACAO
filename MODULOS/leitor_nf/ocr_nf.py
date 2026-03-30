import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\TESSDATA"

def rodar_ocr(caminho_arquivo):
    img = cv2.imread(caminho_arquivo)

    if img is None:
        raise ValueError("Arquivo nao pode ser lido: " + caminho_arquivo)

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

    texto = pytesseract.image_to_string(
        thresh,
        lang="por",
        config="--oem 3 --psm 4"
    )

    return texto