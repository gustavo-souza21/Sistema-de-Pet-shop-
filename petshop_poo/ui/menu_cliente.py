"""
ui/menu_cliente.py
Submenu textual (terminal) para as operacoes de Cliente.
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from services.cliente_service import ClienteService


def _ler_opcional(rotulo):
    valor = input(f"{rotulo} (Enter para deixar em branco): ").strip()
    return valor or None


def menu_cliente():
    service = ClienteService()

    while True:
        print("\n--- CLIENTES ---")
        print("1. Cadastrar novo cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por codigo")
        print("4. Atualizar cliente")
        print("5. Remover cliente")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome: ").strip()
                cpf = _ler_opcional("CPF (11 numeros)")
                endereco = _ler_opcional("Endereco")
                email = _ler_opcional("Email")
                fone = _ler_opcional("Fone")
                cliente = service.cadastrar(nome, cpf, endereco, email, fone)
                print(f"Cliente criado com sucesso: {cliente}")

            elif opcao == "2":
                clientes = service.listar_todos()
                if not clientes:
                    print("Nenhum cliente cadastrado.")
                for c in clientes:
                    print(c)

            elif opcao == "3":
                cod = int(input("Codigo do cliente: ").strip())
                print(service.buscar(cod))

            elif opcao == "4":
                cod = int(input("Codigo do cliente a atualizar: ").strip())
                nome = _ler_opcional("Novo nome")
                cpf = _ler_opcional("Novo CPF (11 numeros)")
                endereco = _ler_opcional("Novo endereco")
                email = _ler_opcional("Novo email")
                fone = _ler_opcional("Novo fone")
                atualizado = service.atualizar(cod, nome=nome, cpf=cpf, endereco=endereco, email=email, fone=fone)
                print(f"Atualizado: {atualizado}")

            elif opcao == "5":
                cod = int(input("Codigo do cliente a remover: ").strip())
                service.remover(cod)
                print("Cliente removido com sucesso.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
