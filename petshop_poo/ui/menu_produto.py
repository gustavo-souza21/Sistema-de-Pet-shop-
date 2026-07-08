"""
ui/menu_produto.py
Submenu textual (terminal) para as operacoes de Produto, incluindo a
baixa manual de estoque (regra de negocio orientada a objetos definida
em models/produto.py).
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from models.produto import Produto
from repositories.produto_repository import ProdutoRepository


def menu_produto():
    repositorio = ProdutoRepository()

    while True:
        print("\n--- PRODUTOS ---")
        print("1. Cadastrar novo produto")
        print("2. Listar produtos")
        print("3. Dar baixa manual no estoque")
        print("4. Remover produto")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome do produto: ").strip()
                preco = float(input("Preco: ").strip())
                estoque = int(input("Estoque inicial: ").strip() or "0")
                produto = Produto(nome=nome, preco=preco, estoque=estoque)
                criado = repositorio.criar(produto)
                print(f"Produto criado: {criado}")

            elif opcao == "2":
                for p in repositorio.listar():
                    print(p)

            elif opcao == "3":
                cod = int(input("Codigo do produto: ").strip())
                quantidade = int(input("Quantidade para baixar: ").strip())
                produto = repositorio.buscar_por_id(cod)
                if produto is None:
                    print("Produto nao encontrado.")
                    continue
                produto.baixar_estoque(quantidade)  # regra de negocio no proprio objeto
                repositorio.atualizar(cod, estoque=produto.estoque)
                print(f"Baixa realizada. Estoque atual: {produto.estoque}")

            elif opcao == "4":
                cod = int(input("Codigo do produto a remover: ").strip())
                removido = repositorio.deletar(cod)
                print("Removido com sucesso." if removido else "Produto nao encontrado.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
