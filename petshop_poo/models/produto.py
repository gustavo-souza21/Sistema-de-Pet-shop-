from models.excecoes import EstoqueInsuficienteError


class Produto:
    def __init__(self, nome, preco, estoque=0, cod=None):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.cod = cod

    def baixar_estoque(self, quantidade):
        """
        Diminui o estoque em memoria em 'quantidade' unidades.
        Levanta EstoqueInsuficienteError se isso deixaria o estoque negativo.
        Quem chamar este metodo ainda precisa persistir a mudanca via
        repository (este metodo so protege a regra do lado do objeto).
        """
        if quantidade <= 0:
            raise ValueError("Quantidade para baixa deve ser maior que zero.")
        if quantidade > self.estoque:
            raise EstoqueInsuficienteError(self.nome, self.estoque, quantidade)
        self.estoque -= quantidade
        return self.estoque

    def __str__(self):
        return f"[{self.cod}] {self.nome} - R$ {self.preco:.2f} (estoque: {self.estoque})"

    def to_dict(self):
        return {"nome": self.nome, "preco": self.preco, "estoque": self.estoque}

    @classmethod
    def from_dict(cls, row):
        return cls(
            nome=row["nome"],
            preco=row["preco"],
            estoque=row.get("estoque", 0),
            cod=row.get("id_produto"),
        )
