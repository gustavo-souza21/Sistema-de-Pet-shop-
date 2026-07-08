"""
models/animal.py
Classe de dominio Animal. Nao herda de Pessoa (um animal nao e uma
pessoa), mas se relaciona com Cliente atraves de id_cliente (o tutor).
"""


class Animal:
    def __init__(self, nome, id_cliente, especie=None, data_nascimento=None, cod=None, nome_tutor=None):
        self.cod = cod
        self.nome = nome
        self.especie = especie
        self.data_nascimento = data_nascimento
        self.id_cliente = id_cliente
        self.nome_tutor = nome_tutor  # preenchido so quando vem de uma consulta com JOIN

    def __str__(self):
        tutor = f", tutor: {self.nome_tutor}" if self.nome_tutor else ""
        especie = f" ({self.especie})" if self.especie else ""
        return f"[{self.cod}] {self.nome}{especie}{tutor}"

    def to_dict(self):
        return {
            "nome": self.nome,
            "especie": self.especie,
            "data_nascimento": self.data_nascimento,
            "id_cliente": self.id_cliente,
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            nome=row["nome"],
            id_cliente=row.get("id_cliente"),
            especie=row.get("especie"),
            data_nascimento=row.get("data_nascimento"),
            cod=row.get("cod_animal"),
            nome_tutor=row.get("nome_tutor"),
        )
