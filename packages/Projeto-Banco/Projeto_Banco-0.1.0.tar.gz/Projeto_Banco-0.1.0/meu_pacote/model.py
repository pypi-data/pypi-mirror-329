from datetime import datetime
import re
import os


class Usuario():
    def __init__(self,titular, data_nascimento, cpf, endereco):
        self.titular = titular
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class salvar_usuario_em_arquivo():
    def __init__(self, usuario, usuarios = "usuarios.txt"):
        self.usuario = usuario
        self.usuario = usuarios

        if os.name == 'posix':
            usuarios = "/home/hidan/Documentos/GitHub/Dio---desafio-1/usuarios.txt"
        elif os.name == 'nt':
            usuarios = "C:\\Users\\hidan\\Documents\\GitHub\\Dio---desafio-1\\usuarios.txt"
        else:
            print("Sistema operacional não suportado.")
            return

        with open(usuarios, "a") as file:
            file.write(f"Titular: {self.usuario.titular}, Data de Nascimento: {self.usuario.data_nascimento}, CPF: {self.usuario.cpf}, Endereço: {self.usuario.endereco}\n")
            print(f"Usuário {self.usuario.titular} salvo com sucesso!")
        

class Conta:
    def __init__(self, usuario, saldo=0, agencia = "0001"):
        self.usuario = usuario
        self.saldo = saldo
        self.agencia = agencia
        self.extrato = []
        self.saques_realizados = 0 
        self.transacoes = 0
        self.transacoes_limite = 10
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def atualizar_transacoes(self):
        if (self.transacoes) >= self.transacoes_limite:
            print(f"Erro: Limite diário de transações atingido para sua conta {self.usuario.nome}.")
            return False
        return True

    def atualizar_data(self):
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def depositar(self, valor):
        if not self.atualizar_transacoes():
            return False

        try:
            valor = float(valor)
            if valor > 0:
                self.saldo += valor
                self.atualizar_data()
              
                self.transacoes+= 1
                self.extrato.append(f'Depósito: R$ {valor:.2f}, Data: {self.data}')
                print(f'Depósito de R$ {valor:.2f} realizado com sucesso!')
            else:
                print("O valor do depósito precisa ser positivo.")
        except ValueError:
            print('Erro: Valor inválido para depósito.')

    def sacar(self, valor):

        if not self.atualizar_transacoes():
            return False
        
        try:
            
            LIMITE_SAQUES = 3
            SAQUE_MAXIMO = 500

            valor = float(valor)

            if self.saques_realizados >= LIMITE_SAQUES:
                print("Erro: Limite diário de saques atingido.")
                return
            
            if valor > self.saldo:
                print(f"Erro: Saldo insuficiente Saldo atual de: R$ {self.saldo:.2f}")
                return
            
            if valor < 0:
                print("Erro: O valor do saque deve ser positivo.")
                return

            if valor > SAQUE_MAXIMO:
                print(f"Erro: O valor máximo para saque é de R$ {SAQUE_MAXIMO:.2f} por operação.")
                return

            if valor > 0:
                self.saldo -= valor
                self.atualizar_data()
                self.transacoes+= 1
                self.extrato.append(f'Saque: R$ {valor:.2f}, Data: {self.data}')
                self.saques_realizados += 1
                print(f'Saque de R$ {valor:.2f} realizado com sucesso!')
            else:
                print("Erro: O valor do saque deve ser maior que zero.")

        except ValueError:
            print('Erro: Valor inválido para saque.')

    def mostrar_extrato(self):
        print(f"\nExtrato da conta de {self.usuario.titular}:")  
        print(f"Saldo atual: R$ {self.saldo:.2f}")   
        if self.extrato:
            for transacao in self.extrato:  
                print(transacao)
        else:
            print("Nenhuma operação realizada ainda.")

    @staticmethod
    def listar_contas(contas):
        """ Lista todas as contas cadastradas. """
        for conta in contas:
            print(f"Titular: {conta.usuario.titular}, Saldo: R$ {conta.saldo:.2f} CPF: {conta.usuario.cpf}")


    @staticmethod
    def buscar_conta(cpf, contas):
        """ Busca uma conta pelo nome do cpf. """
        for conta in contas:
            if conta.usuario.cpf == cpf:
                return conta
        return None
    
    @staticmethod
    def validar_data_nascimento(data_nascimento):
        try:
            datetime.strptime(data_nascimento, "%d/%m/%Y")
            return True
        except Exception as e:
            return False
    @staticmethod
    def validar_cpf(cpf):
        try:
            regex_cpf = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
            if regex_cpf.match(cpf):
                return True  
        except:
            return False   