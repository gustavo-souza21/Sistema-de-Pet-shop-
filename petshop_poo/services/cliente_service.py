"""
services/cliente_service.py
Regras de negocio da entidade Cliente. A regra pedida pelo edital
("nao permitir cadastro repetido por e-mail") vive aqui, e nao no
repository nem no model -- o service e a camada que orquestra
repository + regras.
"""

from models.cliente import Cliente
from models.excecoes import ClienteNaoEncontradoError, EmailDuplicadoError
from repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, repositorio: ClienteRepository = None):
        self.repositorio = repositorio or ClienteRepository()

    def cadastrar(self, nome, cpf=None, endereco=None, email=None, fone=None) -> Cliente:
        if email:
            ja_existe = any(
                c.email and c.email.lower() == email.lower()
                for c in self.repositorio.listar()
            )
            if ja_existe:
                raise EmailDuplicadoError(email)

        # cliente.cpf ja valida o formato (11 numeros) via encapsulamento em Pessoa;
        # a unicidade do CPF (nao repetir entre clientes) e garantida pelo banco.
        cliente = Cliente(nome=nome, cpf=cpf, endereco=endereco, email=email, fone=fone)
        return self.repositorio.criar(cliente)

    def listar_todos(self):
        return self.repositorio.listar()

    def buscar(self, cod_cliente) -> Cliente:
        cliente = self.repositorio.buscar_por_id(cod_cliente)
        if cliente is None:
            raise ClienteNaoEncontradoError(cod_cliente)
        return cliente

    def atualizar(self, cod_cliente, nome=None, cpf=None, endereco=None, email=None, fone=None) -> Cliente:
        if email:
            conflito = any(
                c.email and c.email.lower() == email.lower() and c.cod != cod_cliente
                for c in self.repositorio.listar()
            )
            if conflito:
                raise EmailDuplicadoError(email)

        if cpf is not None:
            # reaproveita a validacao de formato (11 numeros) da classe Cliente/Pessoa
            cpf = Cliente(nome="validacao_temporaria", cpf=cpf).cpf

        atualizado = self.repositorio.atualizar(
            cod_cliente, nome=nome, cpf=cpf, endereco=endereco, email=email, fone=fone
        )
        if atualizado is None:
            raise ClienteNaoEncontradoError(cod_cliente)
        return atualizado

    def remover(self, cod_cliente) -> bool:
        removido = self.repositorio.deletar(cod_cliente)
        if not removido:
            raise ClienteNaoEncontradoError(cod_cliente)
        return True
