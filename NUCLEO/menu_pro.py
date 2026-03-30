import sys
import os

# Garantir que Python encontra o motor
sys.path.append(os.path.join(os.path.dirname(__file__), "../MOTOR"))
import motor_minimo_pro as motor

def menu():
    while True:
        print("\nMENU PRINCIPAL PRO")
        print("1 - Listar empresas")
        print("2 - Criar empresa")
        print("3 - Carregar módulos")
        print("4 - Listar módulos")
        print("5 - Executar módulo")
        print("6 - Financeiro")
        print("0 - Sair")
        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "1":
            motor.listar_empresas()
        elif escolha == "2":
            motor.criar_empresa()
        elif escolha == "3":
            motor.carregar_modulos()
        elif escolha == "4":
            motor.listar_modulos()
        elif escolha == "5":
            emp_id = input("Escolha a empresa pelo ID: ").strip()
            nome_modulo = input("Nome do módulo (sem .py): ").strip()
            motor.executar_modulo(emp_id, nome_modulo)
        elif escolha == "6":
            emp_id = input("Escolha a empresa pelo ID: ").strip()
            motor.financeiro(emp_id)
        elif escolha == "0":
            print("Saindo do sistema")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    print("Motor iniciado com sucesso")
    motor.iniciar()
    menu()