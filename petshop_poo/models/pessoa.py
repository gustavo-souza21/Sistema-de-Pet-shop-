from abc import ABC, abstractmethod

from models.excecoes import CpfInvalidoError


class Pessoa(ABC):
    def __init__(self, nome, cpf=None, cod=None):
        self._cod = cod
        self.nome = nome  # passa pelo setter/validacao abaixo
        self.cpf = cpf    # idem

    # --- encapsulamento: cod e somente-leitura (gerado pelo banco) ----------
    @property
    def cod(self):
        return self._cod

    @cod.setter
    def cod(self, valor):
        self._cod = valor

    # --- encapsulamento: nome nunca pode ficar vazio -------------------------
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome nao pode ser vazio.")
        self._nome = valor.strip()

    # --- encapsulamento: CPF, quando informado, precisa ter exatamente ------
    # --- 11 numeros (formatacao como pontos/traco e aceita e removida) ------
    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        if valor is None or valor == "":
            self._cpf = None
            return

        apenas_digitos = "".join(caractere for caractere in str(valor) if caractere.isdigit())
        if len(apenas_digitos) != 11:
            raise CpfInvalidoError(valor)

        self._cpf = apenas_digitos

    @abstractmethod
    def descricao_papel(self):
        """Retorna uma string curta descrevendo o papel desta pessoa (ex: 'Cliente')."""
        raise NotImplementedError

    def __str__(self):
        identificador = self.cod if self.cod is not None else "novo"
        return f"[{identificador}] {self.descricao_papel()}: {self.nome}"
