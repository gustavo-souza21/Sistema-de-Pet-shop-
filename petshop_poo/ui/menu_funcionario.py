"""
ui/menu_funcionario.py
Submenu textual (terminal) para Funcionario e suas especializacoes
(Veterinario / Tosador).
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from models.funcionario import Funcionario
from repositories.funcionario_repository import FuncionarioRepository


def menu_funcionario():
    repositorio = FuncionarioRepository()

    while True:
        print("\n--- FUNCIONARIOS ---")
        print("1. Cadastrar novo funcionario")
        print("2. Listar funcionarios (com especializacoes)")
        print("3. Tornar funcionario veterinario")
        print("4. Tornar funcionario tosador")
        print("5. Remover funcionario")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome: ").strip()
                cpf = input("CPF (11 numeros, Enter para deixar em branco): ").strip() or None
                cargo = input("Cargo (Enter para deixar em branco): ").strip() or None
                funcionario = Funcionario(nome=nome, cpf=cpf, cargo=cargo)
                criado = repositorio.criar(funcionario)
                print(f"Funcionario criado: {criado}")

            elif opcao == "2":
                for f in repositorio.listar():
                    print(f)

            elif opcao == "3":
                cod = int(input("Codigo do funcionario: ").strip())
                crmv = input("CRMV: ").strip()
                repositorio.tornar_veterinario(cod, crmv)
                print("Funcionario agora e veterinario.")

            elif opcao == "4":
                cod = int(input("Codigo do funcionario: ").strip())
                especialidade = input("Especialidade (Enter para deixar em branco): ").strip() or None
                repositorio.tornar_tosador(cod, especialidade)
                print("Funcionario agora e tosador.")

            elif opcao == "5":
                cod = int(input("Codigo do funcionario a remover: ").strip())
                removido = repositorio.deletar(cod)
                print("Removido com sucesso." if removido else "Funcionario nao encontrado.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
