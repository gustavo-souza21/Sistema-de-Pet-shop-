"""
services/animal_service.py
Regras de negocio da entidade Animal.
"""

from models.animal import Animal
from models.excecoes import AnimalNaoEncontradoError, ClienteNaoEncontradoError
from repositories.animal_repository import AnimalRepository
from repositories.cliente_repository import ClienteRepository


class AnimalService:
    def __init__(self, repositorio: AnimalRepository = None, cliente_repositorio: ClienteRepository = None):
        self.repositorio = repositorio or AnimalRepository()
        self.cliente_repositorio = cliente_repositorio or ClienteRepository()

    def cadastrar(self, nome, id_cliente, especie=None, data_nascimento=None) -> Animal:
        # regra de negocio: o tutor precisa existir antes de cadastrar o animal
        if self.cliente_repositorio.buscar_por_id(id_cliente) is None:
            raise ClienteNaoEncontradoError(id_cliente)

        animal = Animal(nome=nome, id_cliente=id_cliente, especie=especie, data_nascimento=data_nascimento)
        return self.repositorio.criar(animal)

    def listar_todos(self):
        return self.repositorio.listar()

    def listar_por_cliente(self, id_cliente):
        return self.repositorio.listar_por_cliente(id_cliente)

    def buscar(self, cod_animal) -> Animal:
        animal = self.repositorio.buscar_por_id(cod_animal)
        if animal is None:
            raise AnimalNaoEncontradoError(cod_animal)
        return animal

    def atualizar(self, cod_animal, nome=None, especie=None, data_nascimento=None, id_cliente=None) -> Animal:
        if id_cliente is not None and self.cliente_repositorio.buscar_por_id(id_cliente) is None:
            raise ClienteNaoEncontradoError(id_cliente)

        atualizado = self.repositorio.atualizar(
            cod_animal, nome=nome, especie=especie, data_nascimento=data_nascimento, id_cliente=id_cliente
        )
        if atualizado is None:
            raise AnimalNaoEncontradoError(cod_animal)
        return atualizado

    def remover(self, cod_animal) -> bool:
        removido = self.repositorio.deletar(cod_animal)
        if not removido:
            raise AnimalNaoEncontradoError(cod_animal)
        return True
