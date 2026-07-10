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
