from model import Conta, Usuario, salvar_usuario_em_arquivo
from datetime import datetime


transacoes_diarias = 0
ultima_transacao = datetime.today().date()

def ui():
    contas = []
    global transacoes_diarias, ultima_transacao
    
    while True:
        try:
            
            if datetime.today().date() != ultima_transacao:
                ultima_transacao = datetime.today().date()
                transacoes_diarias = 0
                print("Limite diário de transações resetado.")

            if transacoes_diarias >= 10:
                print("Erro: Limite diário de transações atingido.")    
                print("Deseja sair do sistema ou continuar?")
                opcao = input("Digite 1 para sair ou 2 para continuar: ")
                if opcao == "1":
                    print("Saindo do sistema...")
                    break
                continue

            print("\n=== MENU ===")
            print("1. Criar conta")
            print("2. Depositar")
            print("3. Sacar")
            print("4. Extrato")
            print("5. Listar contas Cadastradas")
            print("6. Salvar conta do usuario em arquivo")
            print("7. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                if transacoes_diarias >= 10:
                    print("Erro: Limite diário de transações atingido.")
                else:    
                    titular = input("Digite o nome do titular: ").strip()
                    saldo = float(input("Digite o saldo inicial: "))
                    data_nascimento = input("Digite a data de nascimento formato 00/00/0000: ")
                    cpf = input("Digite o CPF no formato 000.000.000-00: ").strip()

                    if any(conta.usuario.cpf == cpf for conta in contas):
                        print("Erro: Já existe uma conta com esse CPF.")
                        continue

                    if not Conta.validar_data_nascimento(data_nascimento) or not Conta.validar_cpf(cpf):
                        print("Erro: Data de nascimento ou CPF inválidos.")
                        continue
                        
                    endereco = input("Digite o endereço nesse formato: 'logradouro, numero, bairro, cidade, estado, cep': ") .split(',')   


                    usuarios = Usuario(titular, data_nascimento, cpf, endereco)
                    conta = Conta(usuarios, saldo, agencia= "0001")
                    contas.append(conta)
                    
                    print(f"Conta criada para {titular}!")
                    transacoes_diarias += 1

            elif opcao == "2":
                if transacoes_diarias >= 10:
                    print("Erro: Limite diário de transações atingido.")

                cpf = input("Digite seu cpf do titular: ").strip()
                conta = Conta.buscar_conta(cpf, contas)
                
                if conta:
                    valor = input("Digite o valor do depósito: ")
                    conta.depositar(valor)
                    transacoes_diarias += 1
                else:
                    print("Erro: Conta não encontrada.")

            elif opcao == "3":
                cpf = input("Digite seu cpf do titular: ").strip()
                conta = Conta.buscar_conta(cpf, contas)
                if conta:
                    valor = input("Digite o valor do saque: ")
                    conta.sacar(valor)
                    transacoes_diarias += 1
                else:
                    print("Erro: Conta não encontrada.")

            elif opcao == "4":
                cpf = input("Digite o numero do cpf da conta: ").strip()
                conta = Conta.buscar_conta(cpf, contas)
                if conta:
                    conta.mostrar_extrato()
                    transacoes_diarias += 1
                else:
                    print("Erro: Conta não encontrada.")

            elif opcao == "5":
                print("Listando contas")
                Conta.listar_contas(contas)
            elif opcao == "6":
                cpf = input("Digite o CPF do titular: ").strip()
                conta = Conta.buscar_conta(cpf, contas)
                if conta:
                    salvar_usuario_em_arquivo(conta.usuario)
                    print("Conta salva em arquivo com sucesso.")
                else:
                    print("Erro: Conta não encontrada.")
            elif opcao == "7":
                print("Saindo do sistema...")      
                break  

            print(f"Transações diárias: {transacoes_diarias}")      

        except Exception as e:
            print(f"Erro: {e}")
