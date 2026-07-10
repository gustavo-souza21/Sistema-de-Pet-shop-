class Servico:
    def __init__(self, tipo_servico, valor, cod=None):
        self.tipo_servico = tipo_servico
        self.valor = valor
        self.cod = cod

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        if novo_valor is not None and novo_valor < 0:
            raise ValueError("Valor do servico nao pode ser negativo.")
        self._valor = novo_valor

    def __str__(self):
        return f"[{self.cod}] {self.tipo_servico} - R$ {self.valor:.2f}"

    def to_dict(self):
        return {"tipo_servico": self.tipo_servico, "valor": self.valor}

    @classmethod
    def from_dict(cls, row):
        return cls(
            tipo_servico=row["tipo_servico"],
            valor=row["valor"],
            cod=row.get("id_servico"),
        )
