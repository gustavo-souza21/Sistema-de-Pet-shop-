"""
ui/menu_venda.py
Submenu textual (terminal) para as operacoes de Venda. Ao detalhar uma
venda, os itens (ItemServico e ItemProduto) sao impressos com o mesmo
laco `for item in venda.itens: print(item)` -- e o polimorfismo de
ItemBase.subtotal()/descricao() em acao.
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from services.venda_service import VendaService


def menu_venda():
    service = VendaService()

    while True:
        print("\n--- VENDAS ---")
        print("1. Abrir nova venda")
        print("2. Adicionar produto a uma venda")
        print("3. Adicionar servico (via agendamento) a uma venda")
        print("4. Detalhar venda (ver itens)")
        print("5. Listar vendas")
        print("6. Remover venda")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                id_cliente_str = input("Codigo do cliente (Enter para venda avulsa): ").strip()
                id_agendamento_str = input("Codigo do agendamento de origem (Enter se nao houver): ").strip()
                venda = service.abrir_venda(
                    id_cliente=int(id_cliente_str) if id_cliente_str else None,
                    id_agendamento=int(id_agendamento_str) if id_agendamento_str else None,
                )
                print(f"Venda aberta: {venda}")

            elif opcao == "2":
                id_venda = int(input("Codigo da venda: ").strip())
                id_produto = int(input("Codigo do produto: ").strip())
                quantidade = int(input("Quantidade: ").strip())
                item = service.adicionar_produto(id_venda, id_produto, quantidade)
                print(f"Item adicionado: {item}")

            elif opcao == "3":
                id_venda = int(input("Codigo da venda: ").strip())
                id_agendamento = int(input("Codigo do agendamento: ").strip())
                valor_unitario = float(input("Valor do servico: ").strip())
                item = service.adicionar_servico(id_venda, id_agendamento, valor_unitario)
                print(f"Item adicionado: {item}")

            elif opcao == "4":
                id_venda = int(input("Codigo da venda: ").strip())
                venda = service.detalhar(id_venda)
                print(venda)
                for item in venda.itens:
                    print(f"  - {item}")
                print(f"Total calculado em memoria: R$ {venda.calcular_total():.2f}")

            elif opcao == "5":
                for v in service.listar_todas():
                    print(v)

            elif opcao == "6":
                id_venda = int(input("Codigo da venda a remover: ").strip())
                service.remover(id_venda)
                print("Venda removida com sucesso.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
