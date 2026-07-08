"""
repositories/agendamento_repository.py
Acesso ao banco para a entidade Agendamento. Tres FKs obrigatorias
(Cod_animal, Id_funcionario, Id_servico) -- qualquer uma inexistente
estoura ForeignKeyViolation na criacao ou atualizacao.
"""

import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.agendamento import Agendamento
from models.excecoes import RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class AgendamentoRepository(RepositorioBase):
    def criar(self, agendamento: Agendamento) -> Agendamento:
        sql = """
            INSERT INTO Agendamento (Data, Hora, Status, Cod_animal, Id_funcionario, Id_servico)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING Id_agendamento, Data, Hora, Status, Cod_animal, Id_funcionario, Id_servico;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (
                    agendamento.data, agendamento.hora, agendamento.status,
                    agendamento.cod_animal, agendamento.id_funcionario, agendamento.id_servico,
                ))
                row = cur.fetchone()
            conn.commit()
            return Agendamento.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        sql = """
            SELECT
                ag.Id_agendamento, ag.Data, ag.Hora, ag.Status,
                ag.Cod_animal, an.Nome AS nome_animal,
                cl.Nome AS nome_tutor,
                ag.Id_funcionario, f.Nome AS nome_funcionario,
                ag.Id_servico, s.Tipo_servico, s.Valor AS valor_servico
            FROM Agendamento ag
            JOIN Animal an ON an.Cod_animal = ag.Cod_animal
            JOIN Cliente cl ON cl.Cod_cliente = an.Id_cliente
            JOIN Funcionario f ON f.Id_funcionario = ag.Id_funcionario
            JOIN Servico s ON s.Id_servico = ag.Id_servico
            ORDER BY ag.Data, ag.Hora;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Agendamento.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def listar_por_status(self, status):
        sql = """
            SELECT
                ag.Id_agendamento, ag.Data, ag.Hora, ag.Status,
                ag.Cod_animal, an.Nome AS nome_animal,
                ag.Id_funcionario, f.Nome AS nome_funcionario,
                ag.Id_servico, s.Tipo_servico
            FROM Agendamento ag
            JOIN Animal an ON an.Cod_animal = ag.Cod_animal
            JOIN Funcionario f ON f.Id_funcionario = ag.Id_funcionario
            JOIN Servico s ON s.Id_servico = ag.Id_servico
            WHERE ag.Status = %s
            ORDER BY ag.Data, ag.Hora;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (status,))
                return [Agendamento.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def listar_por_funcionario_data(self, id_funcionario, data):
        """Usado pela regra de negocio que impede dois agendamentos no mesmo horario."""
        sql = """
            SELECT Id_agendamento, Data, Hora, Status, Cod_animal, Id_funcionario, Id_servico
            FROM Agendamento
            WHERE Id_funcionario = %s AND Data = %s AND Status != 'Cancelado';
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_funcionario, data))
                return [Agendamento.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, id_agendamento):
        sql = """
            SELECT Id_agendamento, Data, Hora, Status, Cod_animal, Id_funcionario, Id_servico
            FROM Agendamento WHERE Id_agendamento = %s;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_agendamento,))
                row = cur.fetchone()
                return Agendamento.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, id_agendamento, data=None, hora=None, status=None,
                   cod_animal=None, id_funcionario=None, id_servico=None):
        campos, valores = [], []
        if data is not None:
            campos.append("Data = %s")
            valores.append(data)
        if hora is not None:
            campos.append("Hora = %s")
            valores.append(hora)
        if status is not None:
            campos.append("Status = %s")
            valores.append(status)
        if cod_animal is not None:
            campos.append("Cod_animal = %s")
            valores.append(cod_animal)
        if id_funcionario is not None:
            campos.append("Id_funcionario = %s")
            valores.append(id_funcionario)
        if id_servico is not None:
            campos.append("Id_servico = %s")
            valores.append(id_servico)

        if not campos:
            return self.buscar_por_id(id_agendamento)

        sql = f"""
            UPDATE Agendamento SET {', '.join(campos)}
            WHERE Id_agendamento = %s
            RETURNING Id_agendamento, Data, Hora, Status, Cod_animal, Id_funcionario, Id_servico;
        """
        valores.append(id_agendamento)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Agendamento.from_dict(row) if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, id_agendamento):
        sql = "DELETE FROM Agendamento WHERE Id_agendamento = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_agendamento,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Agendamento", id_agendamento)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
