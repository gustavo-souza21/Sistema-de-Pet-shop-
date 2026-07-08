"""
models/funcionario.py
Classe de dominio Funcionario. Tambem herda de Pessoa, mas implementa
'descricao_papel' de forma bem diferente de Cliente -- e exatamente
esse contraste que caracteriza o polimorfismo: o mesmo metodo
(descricao_papel / __str__, herdado de Pessoa) se comporta de forma
diferente dependendo da classe concreta.

Um funcionario pode acumular as especializacoes de Veterinario e/ou
Tosador (tabelas independentes no banco, sem exclusividade mutua).
Aqui isso e representado por dois atributos opcionais (crmv,
especialidade) que ficam None quando a especializacao nao se aplica.
"""

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
