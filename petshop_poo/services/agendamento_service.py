from models.agendamento import Agendamento
from models.excecoes import AgendamentoNaoEncontradoError, HorarioIndisponivelError
from repositories.agendamento_repository import AgendamentoRepository


class AgendamentoService:
    def __init__(self, repositorio: AgendamentoRepository = None):
        self.repositorio = repositorio or AgendamentoRepository()

    def agendar(self, data, hora, cod_animal, id_funcionario, id_servico, status="Agendado") -> Agendamento:
        agendamentos_do_dia = self.repositorio.listar_por_funcionario_data(id_funcionario, data)
        if any(ag.hora == hora for ag in agendamentos_do_dia):
            raise HorarioIndisponivelError(id_funcionario, data, hora)

        agendamento = Agendamento(
            data=data, hora=hora, cod_animal=cod_animal,
            id_funcionario=id_funcionario, id_servico=id_servico, status=status,
        )
        return self.repositorio.criar(agendamento)

    def listar_todos(self):
        return self.repositorio.listar()

    def listar_por_status(self, status):
        return self.repositorio.listar_por_status(status)

    def buscar(self, id_agendamento) -> Agendamento:
        agendamento = self.repositorio.buscar_por_id(id_agendamento)
        if agendamento is None:
            raise AgendamentoNaoEncontradoError(id_agendamento)
        return agendamento

    def mudar_status(self, id_agendamento, novo_status) -> Agendamento:
        agendamento_atual = self.buscar(id_agendamento)
        agendamento_atual.status = novo_status

        atualizado = self.repositorio.atualizar(id_agendamento, status=agendamento_atual.status)
        if atualizado is None:
            raise AgendamentoNaoEncontradoError(id_agendamento)
        return atualizado

    def remover(self, id_agendamento) -> bool:
        removido = self.repositorio.deletar(id_agendamento)
        if not removido:
            raise AgendamentoNaoEncontradoError(id_agendamento)
        return True
