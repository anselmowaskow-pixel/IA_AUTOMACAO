import xml.etree.ElementTree as ET

def extrair_dados_xml(caminho_xml):
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

    dados = {
        "tipo": "NFE-XML",
        "numero": "",
        "emitente": "",
        "cnpj_emitente": "",
        "valor_total": "",
        "chave": ""
    }

    tree = ET.parse(caminho_xml)
    root = tree.getroot()

    nNF = root.find(".//nfe:ide/nfe:nNF", ns)
    if nNF is not None:
        dados["numero"] = nNF.text

    emit = root.find(".//nfe:emit/nfe:xNome", ns)
    if emit is not None:
        dados["emitente"] = emit.text

    cnpj = root.find(".//nfe:emit/nfe:CNPJ", ns)
    if cnpj is not None:
        dados["cnpj_emitente"] = cnpj.text

    total = root.find(".//nfe:ICMSTot/nfe:vNF", ns)
    if total is not None:
        dados["valor_total"] = total.text

    inf = root.find(".//nfe:infNFe", ns)
    if inf is not None and "Id" in inf.attrib:
        dados["chave"] = inf.attrib["Id"].replace("NFe", "")

    return dados