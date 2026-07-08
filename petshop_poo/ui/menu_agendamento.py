"""
ui/menu_agendamento.py
Submenu textual (terminal) para as operacoes de Agendamento.
"""

from models.excecoes import RegraDeNegocioError, RegistroNaoEncontradoError
from services.agendamento_service import AgendamentoService


def menu_agendamento():
    service = AgendamentoService()

    while True:
        print("\n--- AGENDAMENTOS ---")
        print("1. Criar novo agendamento")
        print("2. Listar todos os agendamentos")
        print("3. Listar por status")
        print("4. Mudar status de um agendamento")
        print("5. Remover agendamento")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                data = input("Data (AAAA-MM-DD): ").strip()
                hora = input("Hora (HH:MM): ").strip()
                cod_animal = int(input("Codigo do animal: ").strip())
                id_funcionario = int(input("Codigo do funcionario: ").strip())
                id_servico = int(input("Codigo do servico: ").strip())
                agendamento = service.agendar(data, hora, cod_animal, id_funcionario, id_servico)
                print(f"Agendamento criado: {agendamento}")

            elif opcao == "2":
                agendamentos = service.listar_todos()
                if not agendamentos:
                    print("Nenhum agendamento cadastrado.")
                for ag in agendamentos:
                    print(ag)

            elif opcao == "3":
                status = input("Status (Agendado/Concluido/Cancelado): ").strip()
                for ag in service.listar_por_status(status):
                    print(ag)

            elif opcao == "4":
                cod = int(input("Codigo do agendamento: ").strip())
                novo_status = input("Novo status (Agendado/Concluido/Cancelado): ").strip()
                atualizado = service.mudar_status(cod, novo_status)
                print(f"Atualizado: {atualizado}")

            elif opcao == "5":
                cod = int(input("Codigo do agendamento a remover: ").strip())
                service.remover(cod)
                print("Agendamento removido com sucesso.")

            elif opcao == "0":
                return

            else:
                print("Opcao invalida.")

        except (RegraDeNegocioError, RegistroNaoEncontradoError, ValueError) as erro:
            print(f"Erro: {erro}")
        except Exception as erro:
            print(f"Erro inesperado ao acessar o banco: {erro}")
