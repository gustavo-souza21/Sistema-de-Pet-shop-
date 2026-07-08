"""
repositories/base_repository.py
Contrato comum de persistencia. Cada repository concreto (Cliente,
Animal, Servico...) herda desta classe abstrata e implementa os cinco
metodos com o SQL especifico da sua tabela. Isso permite, por exemplo,
escrever uma funcao generica que recebe "qualquer RepositorioBase" e
chama .listar() sem precisar saber qual entidade esta por tras --
outro exemplo de polimorfismo no projeto.
"""

from abc import ABC, abstractmethod


class RepositorioBase(ABC):
    @abstractmethod
    def criar(self, entidade):
        """Insere uma nova entidade e retorna o objeto de dominio criado."""
        raise NotImplementedError

    @abstractmethod
    def listar(self):
        """Retorna uma lista de objetos de dominio."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, identificador):
        """Retorna um objeto de dominio, ou None se nao existir."""
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, identificador, **campos):
        """Atualiza apenas os campos informados. Retorna o objeto atualizado ou None."""
        raise NotImplementedError

    @abstractmethod
    def deletar(self, identificador):
        """Remove a entidade. Retorna True se deletou, False se nao existia."""
        raise NotImplementedError
