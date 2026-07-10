from models.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf=None, cargo=None, crmv=None, especialidade=None, cod=None):
        super().__init__(nome, cpf, cod)
        self.cargo = cargo
        self.crmv = crmv
        self.especialidade = especialidade

    @property
    def eh_veterinario(self):
        return self.crmv is not None

    @property
    def eh_tosador(self):
        return self.especialidade is not None

    def descricao_papel(self):
        papeis = []
        if self.eh_veterinario:
            papeis.append("Veterinario")
        if self.eh_tosador:
            papeis.append("Tosador")
        if not papeis:
            papeis.append(self.cargo or "Funcionario")
        return " / ".join(papeis)

    def to_dict(self):
        return {"nome": self.nome, "cpf": self.cpf, "cargo": self.cargo}

    @classmethod
    def from_dict(cls, row):
        return cls(
            nome=row["nome"],
            cpf=row.get("cpf"),
            cargo=row.get("cargo"),
            crmv=row.get("crmv"),
            especialidade=row.get("especialidade"),
            cod=row.get("id_funcionario"),
        )
