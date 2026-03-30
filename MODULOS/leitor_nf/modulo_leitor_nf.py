import re
from datetime import datetime

def limpar_texto(texto):
    texto = texto.upper()
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def extrair_chave_acesso(texto):
    match = re.search(r"CHAVE DE ACESSO\s*([\d\s]{40,60})", texto)
    if match:
        chave = re.sub(r"\D", "", match.group(1))
        if len(chave) == 44:
            return chave
    return None

def extrair_numero_nf(texto):
    match = re.search(r"N[ºO]\s*0*([0-9]{3,})", texto)
    return match.group(1) if match else None

def extrair_data_emissao(texto):
    match = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
    return match.group(1) if match else None

def extrair_cnpj(texto):
    match = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto)
    if match:
        return re.sub(r"\D", "", match.group(1))
    return None

def extrair_cpf(texto):
    match = re.search(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", texto)
    if match:
        return re.sub(r"\D", "", match.group(1))
    return None

def extrair_nome_destinatario(texto):
    match = re.search(r"DESTINAT[ÁA]RIO\s*/\s*REMETENTE\s*(.*?)\s*(CPF|CNPJ)", texto)
    if match:
        nome = match.group(1).strip()
        return nome if len(nome) > 5 else None
    return None

def definir_status(dados):
    obrigatorios = [
        dados.get("numero_nf"),
        dados.get("data_emissao"),
        dados.get("emitente").get("cnpj")
    ]

    if all(obrigatorios):
        return "OK"

    if any(obrigatorios):
        return "ANALISAR"

    return "ILEGIVEL"

def ler_nf_ocr(texto_ocr):
    bruto = texto_ocr
    texto = limpar_texto(texto_ocr)

    chave = extrair_chave_acesso(texto)
    numero_nf = extrair_numero_nf(texto)
    data_emissao = extrair_data_emissao(texto)
    cnpj_emitente = extrair_cnpj(texto)
    cpf_dest = extrair_cpf(texto)
    nome_dest = extrair_nome_destinatario(texto)

    resultado = {
        "tipo_documento": "NF-e",
        "chave_acesso": chave,
        "numero_nf": numero_nf,
        "serie": None,
        "data_emissao": data_emissao,
        "emitente": {
            "cnpj": cnpj_emitente,
            "razao_social": None
        },
        "destinatario": {
            "cpf_cnpj": cpf_dest,
            "nome": nome_dest
        },
        "valor_total_nf": None,
        "status_leitura": None,
        "raw_ocr": bruto
    }

    resultado["status_leitura"] = definir_status(resultado)
    return resultado


# EXECUCAO DIRETA PARA TESTE LOCAL
if __name__ == "__main__":
    from teste_ocr import TEXTO_OCR

    json_nf = ler_nf_ocr(TEXTO_OCR)

    print("\n=== JSON CANONICO NF ===")
    for k, v in json_nf.items():
        print(f"{k}: {v}")