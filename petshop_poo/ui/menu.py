"""
ui/menu.py
Menu principal do sistema, em terminal (texto), conforme pedido pelo
edital do Trabalho Pratico. Cada opcao abre o submenu da entidade
correspondente.
"""

from ui.menu_cliente import menu_cliente
from ui.menu_animal import menu_animal
from ui.menu_servico import menu_servico
from ui.menu_funcionario import menu_funcionario
from ui.menu_agendamento import menu_agendamento
from ui.menu_produto import menu_produto
from ui.menu_venda import menu_venda


def main_menu():
    opcoes = {
        "1": ("Clientes", menu_cliente),
        "2": ("Animais", menu_animal),
        "3": ("Servicos", menu_servico),
        "4": ("Funcionarios", menu_funcionario),
        "5": ("Agendamentos", menu_agendamento),
        "6": ("Produtos", menu_produto),
        "7": ("Vendas", menu_venda),
    }

    while True:
        print("\n===== SISTEMA DE PET SHOP =====")
        for chave, (rotulo, _) in opcoes.items():
            print(f"{chave}. {rotulo}")
        print("0. Sair")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Ate logo!")
            return

        opcao = opcoes.get(escolha)
        if opcao is None:
            print("Opcao invalida.")
            continue

        _, funcao_submenu = opcao
        funcao_submenu()
