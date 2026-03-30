# modulo_objetos.py
def identificar_objeto(imagem_path=None):
    return "identificar_objeto: objeto identificado (placeholder)"

def classificar_material(descricao=None):
    return f"classificar_material: classificado como {descricao}"

def sugerir_reuso(material=None):
    return "sugerir_reuso: possibilidades de reaproveitamento (placeholder)"

if __name__ == '__main__':
    print(identificar_objeto())
    print(classificar_material('plastico'))
