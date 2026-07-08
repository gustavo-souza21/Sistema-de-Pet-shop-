"""
ui/menu_animal.py
Submenu textual (terminal) para as operacoes de Animal.
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from services.animal_service import AnimalService


def _ler_opcional(rotulo):
    valor = input(f"{rotulo} (Enter para deixar em branco): ").strip()
    return valor or None


def menu_animal():
    service = AnimalService()

    while True:
        print("\n--- ANIMAIS ---")
        print("1. Cadastrar novo animal")
        print("2. Listar animais")
        print("3. Buscar animal por codigo")
        print("4. Atualizar animal")
        print("5. Remover animal")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome do animal: ").strip()
                id_cliente = int(input("Codigo do tutor (cliente): ").strip())
                especie = _ler_opcional("Especie")
                data_nascimento = _ler_opcional("Data de nascimento (AAAA-MM-DD)")
                animal = service.cadastrar(nome, id_cliente, especie, data_nascimento)
                print(f"Animal cadastrado com sucesso: {animal}")

            elif opcao == "2":
                animais = service.listar_todos()
                if not animais:
                    print("Nenhum animal cadastrado.")
                for a in animais:
                    print(a)

            elif opcao == "3":
                cod = int(input("Codigo do animal: ").strip())
                print(service.buscar(cod))

            elif opcao == "4":
                cod = int(input("Codigo do animal a atualizar: ").strip())
                nome = _ler_opcional("Novo nome")
                especie = _ler_opcional("Nova especie")
                data_nascimento = _ler_opcional("Nova data de nascimento (AAAA-MM-DD)")
                atualizado = service.atualizar(cod, nome=nome, especie=especie, data_nascimento=data_nascimento)
                print(f"Atualizado: {atualizado}")

            elif opcao == "5":
                cod = int(input("Codigo do animal a remover: ").strip())
                service.remover(cod)
                print("Animal removido com sucesso.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
