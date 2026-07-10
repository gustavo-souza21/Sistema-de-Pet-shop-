from abc import ABC, abstractmethod


class ItemBase(ABC):
    def __init__(self, quantidade, valor_unitario, cod=None):
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.cod = cod

    @abstractmethod
    def subtotal(self):
        raise NotImplementedError

    @abstractmethod
    def descricao(self):
        raise NotImplementedError

    def __str__(self):
        return f"{self.descricao()} x{self.quantidade} = R$ {self.subtotal():.2f}"


class ItemServico(ItemBase):
    def __init__(self, id_agendamento, quantidade, valor_unitario, cod=None, tipo_servico=None):
        super().__init__(quantidade, valor_unitario, cod)
        self.id_agendamento = id_agendamento
        self.tipo_servico = tipo_servico

    def subtotal(self):
        return self.quantidade * self.valor_unitario

    def descricao(self):
        return self.tipo_servico or f"Servico do agendamento {self.id_agendamento}"

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_agendamento=row["id_agendamento"],
            quantidade=row["quantidade"],
            valor_unitario=row["valor_unitario"],
            cod=row.get("id_item_venda"),
            tipo_servico=row.get("tipo_servico"),
        )


class ItemProduto(ItemBase):
    def __init__(self, id_produto, quantidade, valor_unitario, cod=None, nome_produto=None):
        super().__init__(quantidade, valor_unitario, cod)
        self.id_produto = id_produto
        self.nome_produto = nome_produto

    def subtotal(self):
        return self.quantidade * self.valor_unitario

    def descricao(self):
        return self.nome_produto or f"Produto {self.id_produto}"

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_produto=row["id_produto"],
            quantidade=row["quantidade"],
            valor_unitario=row["valor_unitario"],
            cod=row.get("id_item_produto"),
            nome_produto=row.get("nome_produto"),
        )


class Venda:
    def __init__(self, id_cliente=None, id_agendamento=None, valor=0,
                 data=None, cod=None, nome_cliente=None):
        self.id_cliente = id_cliente
        self.id_agendamento = id_agendamento
        self.valor = valor
        self.data = data
        self.cod = cod
        self.nome_cliente = nome_cliente
        self.itens = [] 

    def adicionar_item(self, item: ItemBase):
        self.itens.append(item)

    def calcular_total(self):
        """Soma o subtotal de todos os itens (servicos + produtos), em memoria."""
        return sum(item.subtotal() for item in self.itens)

    def __str__(self):
        cliente = self.nome_cliente or f"cliente {self.id_cliente}"
        return f"[{self.cod}] Venda de {cliente} - R$ {self.valor:.2f}"

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_cliente=row.get("id_cliente"),
            id_agendamento=row.get("id_agendamento"),
            valor=row.get("valor", 0),
            data=row.get("data"),
            cod=row.get("id_venda"),
            nome_cliente=row.get("nome_cliente"),
        )
