"""
models/agendamento.py
Classe de dominio Agendamento. O banco NAO restringe os valores
possiveis de Status (nao ha CHECK no SQL) -- por isso essa validacao
vira uma regra de negocio orientada a objetos aqui: o setter de
'status' so aceita um dos valores de STATUS_PERMITIDOS.
"""

from models.excecoes import StatusInvalidoError

STATUS_PERMITIDOS = ("Agendado", "Concluido", "Cancelado")


class Agendamento:
    def __init__(self, data, hora, cod_animal, id_funcionario, id_servico,
                 status="Agendado", cod=None, nome_animal=None,
                 nome_funcionario=None, tipo_servico=None):
        self.data = data
        self.hora = hora
        self.cod_animal = cod_animal
        self.id_funcionario = id_funcionario
        self.id_servico = id_servico
        self.status = status
        self.cod = cod
        # campos so preenchidos quando o repository faz JOIN (listagem)
        self.nome_animal = nome_animal
        self.nome_funcionario = nome_funcionario
        self.tipo_servico = tipo_servico

    # --- encapsulamento + regra de negocio orientada a objetos ---------------
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        if valor not in STATUS_PERMITIDOS:
            raise StatusInvalidoError(valor, STATUS_PERMITIDOS)
        self._status = valor

    def concluir(self):
        self.status = "Concluido"

    def cancelar(self):
        self.status = "Cancelado"

    def __str__(self):
        animal = self.nome_animal or f"animal {self.cod_animal}"
        return f"[{self.cod}] {self.data} {self.hora} - {animal} - {self.status}"

    def to_dict(self):
        return {
            "data": self.data,
            "hora": self.hora,
            "status": self.status,
            "cod_animal": self.cod_animal,
            "id_funcionario": self.id_funcionario,
            "id_servico": self.id_servico,
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            data=row["data"],
            hora=row["hora"],
            cod_animal=row["cod_animal"],
            id_funcionario=row["id_funcionario"],
            id_servico=row["id_servico"],
            status=row.get("status", "Agendado"),
            cod=row.get("id_agendamento"),
            nome_animal=row.get("nome_animal"),
            nome_funcionario=row.get("nome_funcionario"),
            tipo_servico=row.get("tipo_servico"),
        )
