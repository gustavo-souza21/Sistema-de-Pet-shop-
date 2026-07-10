import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.servico import Servico
from models.excecoes import RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class ServicoRepository(RepositorioBase):
    def criar(self, servico: Servico) -> Servico:
        sql = """
            INSERT INTO Servico (Tipo_servico, Valor)
            VALUES (%s, %s)
            RETURNING Id_servico, Tipo_servico, Valor;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (servico.tipo_servico, servico.valor))
                row = cur.fetchone()
            conn.commit()
            return Servico.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        sql = "SELECT Id_servico, Tipo_servico, Valor FROM Servico ORDER BY Tipo_servico;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Servico.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, id_servico):
        sql = "SELECT Id_servico, Tipo_servico, Valor FROM Servico WHERE Id_servico = %s;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_servico,))
                row = cur.fetchone()
                return Servico.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, id_servico, tipo_servico=None, valor=None):
        campos, valores = [], []
        if tipo_servico is not None:
            campos.append("Tipo_servico = %s")
            valores.append(tipo_servico)
        if valor is not None:
            campos.append("Valor = %s")
            valores.append(valor)

        if not campos:
            return self.buscar_por_id(id_servico)

        sql = f"""
            UPDATE Servico SET {', '.join(campos)}
            WHERE Id_servico = %s
            RETURNING Id_servico, Tipo_servico, Valor;
        """
        valores.append(id_servico)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Servico.from_dict(row) if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, id_servico):
        sql = "DELETE FROM Servico WHERE Id_servico = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_servico,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Servico", id_servico)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
