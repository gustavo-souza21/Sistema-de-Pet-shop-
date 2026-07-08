"""
ui/menu_servico.py
Submenu textual (terminal) para as operacoes de Servico.
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from models.servico import Servico
from repositories.servico_repository import ServicoRepository


def menu_servico():
    repositorio = ServicoRepository()

    while True:
        print("\n--- SERVICOS ---")
        print("1. Cadastrar novo servico")
        print("2. Listar servicos")
        print("3. Atualizar servico")
        print("4. Remover servico")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                tipo_servico = input("Tipo de servico (ex: Banho, Tosa): ").strip()
                valor = float(input("Valor: ").strip())
                servico = Servico(tipo_servico=tipo_servico, valor=valor)
                criado = repositorio.criar(servico)
                print(f"Servico criado: {criado}")

            elif opcao == "2":
                for s in repositorio.listar():
                    print(s)

            elif opcao == "3":
                cod = int(input("Codigo do servico: ").strip())
                tipo_servico = input("Novo tipo (Enter para manter): ").strip() or None
                valor_str = input("Novo valor (Enter para manter): ").strip()
                valor = float(valor_str) if valor_str else None
                atualizado = repositorio.atualizar(cod, tipo_servico=tipo_servico, valor=valor)
                if atualizado is None:
                    print("Servico nao encontrado.")
                else:
                    print(f"Atualizado: {atualizado}")

            elif opcao == "4":
                cod = int(input("Codigo do servico a remover: ").strip())
                removido = repositorio.deletar(cod)
                print("Removido com sucesso." if removido else "Servico nao encontrado.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
