class RegistroNaoEncontradoError(Exception):
    """Base para 'buscar/atualizar algo que nao existe'."""

    def __init__(self, entidade, identificador):
        self.entidade = entidade
        self.identificador = identificador
        super().__init__(f"{entidade} com id={identificador!r} nao encontrado(a).")


class ClienteNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, cod_cliente):
        super().__init__("Cliente", cod_cliente)


class AnimalNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, cod_animal):
        super().__init__("Animal", cod_animal)


class ServicoNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, id_servico):
        super().__init__("Servico", id_servico)


class FuncionarioNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, id_funcionario):
        super().__init__("Funcionario", id_funcionario)


class AgendamentoNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, id_agendamento):
        super().__init__("Agendamento", id_agendamento)


class ProdutoNaoEncontradoError(RegistroNaoEncontradoError):
    def __init__(self, id_produto):
        super().__init__("Produto", id_produto)


class VendaNaoEncontradaError(RegistroNaoEncontradoError):
    def __init__(self, id_venda):
        super().__init__("Venda", id_venda)


class RegraDeNegocioError(Exception):
    """Erro levantado quando uma regra de negocio (nao do banco) e violada."""


class EmailDuplicadoError(RegraDeNegocioError):
    def __init__(self, email):
        self.email = email
        super().__init__(f"Ja existe um cliente cadastrado com o email '{email}'.")


class CpfInvalidoError(RegraDeNegocioError):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"CPF '{cpf}' invalido: deve conter exatamente 11 numeros.")


class CpfDuplicadoError(RegraDeNegocioError):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"Ja existe um cadastro com o CPF '{cpf}'.")


class StatusInvalidoError(RegraDeNegocioError):
    def __init__(self, status, permitidos):
        self.status = status
        self.permitidos = permitidos
        super().__init__(
            f"Status '{status}' invalido. Use um destes: {', '.join(permitidos)}."
        )


class HorarioIndisponivelError(RegraDeNegocioError):
    def __init__(self, id_funcionario, data, hora):
        super().__init__(
            f"O funcionario {id_funcionario} ja tem um agendamento em {data} {hora}."
        )


class EstoqueInsuficienteError(RegraDeNegocioError):
    def __init__(self, nome_produto, estoque_atual, quantidade_solicitada):
        self.nome_produto = nome_produto
        self.estoque_atual = estoque_atual
        self.quantidade_solicitada = quantidade_solicitada
        super().__init__(
            f"Estoque insuficiente de '{nome_produto}': "
            f"disponivel={estoque_atual}, solicitado={quantidade_solicitada}."
        )


class RegistroVinculadoError(RegraDeNegocioError):
    """Levantado quando o banco rejeita um DELETE por causa de uma FK RESTRICT."""

    def __init__(self, entidade, identificador):
        super().__init__(
            f"Nao e possivel excluir {entidade} (id={identificador}): "
            f"existem registros vinculados a ele(a)."
        )
