import os
import json
# Aqui você pode importar sua IA, por exemplo InstrutorVisual, se existir
# from instrutor_visual import processar_imagem

PASTA_FOTOS = "STORAGE/FOTOS/Instrutor Visual"
PASTA_RESULTADOS = "STORAGE/RESULTADOS/Instrutor Visual"

# Certifique-se de criar a pasta de resultados se não existir
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

def processar_fotos():
    fotos = [f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    
    if not fotos:
        print("Nenhuma foto encontrada na pasta.")
        return

    for foto in fotos:
        caminho_foto = os.path.join(PASTA_FOTOS, foto)
        print(f"Processando: {caminho_foto}")

        # Aqui você chamaria a IA real. Exemplo fictício:
        resultado = {
            "foto": foto,
            "descricao": f"Resultado fictício da foto {foto}",
            "objetos_detectados": ["planta", "animal", "placa de trânsito"]
        }
        # Se tiver a IA real, substituir acima por:
        # resultado = processar_imagem(caminho_foto)

        # Salvar resultado em JSON
        arquivo_resultado = os.path.join(PASTA_RESULTADOS, f"{os.path.splitext(foto)[0]}.json")
        with open(arquivo_resultado, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=4)

        print(f"Resultado salvo: {arquivo_resultado}")

    print("Todas as fotos processadas com sucesso.")