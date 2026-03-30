
def identificar_planta():
    print("\n[AGRO] Identificando planta... (placeholder)")
    print("Funcao ainda sera expandida futuramente.\n")

def detectar_doencas():
    print("\n[AGRO] Detectando pragas/doenças... (placeholder)")
    print("Reconhecimento sera implementado depois.\n")

def orientar_adubacao():
    print("\n[AGRO] Orientando adubacao... (placeholder)")
    print("Sugestoes detalhadas serao adicionadas futuramente.\n")

def executar_agro():
    while True:
        print("\n=== MODULO AGRO ===")
        print("1 - Identificar planta")
        print("2 - Detectar doenças / pragas")
        print("3 - Orientar adubacao")
        print("4 - Voltar ao menu principal")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            identificar_planta()
        elif opcao == "2":
            detectar_doencas()
        elif opcao == "3":
            orientar_adubacao()
        elif opcao == "4":
            print("Voltando ao menu principal...")
            break
        else:
            print("Opcao invalida. Tente novamente.")
