from models.pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome, cpf=None, endereco=None, email=None, fone=None, cod=None):
        super().__init__(nome, cpf, cod)
        self.endereco = endereco
        self.email = email
        self.fone = fone

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor is not None and valor != "" and "@" not in valor:
            raise ValueError(f"Email invalido: '{valor}' precisa conter '@'.")
        self._email = valor or None

    def descricao_papel(self):
        return "Cliente"

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "endereco": self.endereco,
            "email": self.email,
            "fone": self.fone,
        }

    @classmethod
    def from_dict(cls, row):
        """Constroi um Cliente a partir de uma linha (dict) vinda do banco."""
        return cls(
            nome=row["nome"],
            cpf=row.get("cpf"),
            endereco=row.get("endereco"),
            email=row.get("email"),
            fone=row.get("fone"),
            cod=row.get("cod_cliente"),
        )
