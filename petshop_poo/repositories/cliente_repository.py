import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.cliente import Cliente
from models.excecoes import CpfDuplicadoError, RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class ClienteRepository(RepositorioBase):
    def criar(self, cliente: Cliente) -> Cliente:
        sql = """
            INSERT INTO Cliente (Nome, Cpf, Endereco, Email, Fone)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING Cod_cliente, Nome, Cpf, Endereco, Email, Fone;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (cliente.nome, cliente.cpf, cliente.endereco, cliente.email, cliente.fone))
                row = cur.fetchone()
            conn.commit()
            return Cliente.from_dict(row)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise CpfDuplicadoError(cliente.cpf)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        sql = "SELECT Cod_cliente, Nome, Cpf, Endereco, Email, Fone FROM Cliente ORDER BY Nome;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Cliente.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, cod_cliente):
        sql = "SELECT Cod_cliente, Nome, Cpf, Endereco, Email, Fone FROM Cliente WHERE Cod_cliente = %s;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (cod_cliente,))
                row = cur.fetchone()
                return Cliente.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, cod_cliente, nome=None, cpf=None, endereco=None, email=None, fone=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("Nome = %s")
            valores.append(nome)
        if cpf is not None:
            campos.append("Cpf = %s")
            valores.append(cpf)
        if endereco is not None:
            campos.append("Endereco = %s")
            valores.append(endereco)
        if email is not None:
            campos.append("Email = %s")
            valores.append(email)
        if fone is not None:
            campos.append("Fone = %s")
            valores.append(fone)

        if not campos:
            return self.buscar_por_id(cod_cliente)

        sql = f"""
            UPDATE Cliente SET {', '.join(campos)}
            WHERE Cod_cliente = %s
            RETURNING Cod_cliente, Nome, Cpf, Endereco, Email, Fone;
        """
        valores.append(cod_cliente)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Cliente.from_dict(row) if row else None
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise CpfDuplicadoError(cpf)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, cod_cliente):
        sql = "DELETE FROM Cliente WHERE Cod_cliente = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (cod_cliente,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Cliente", cod_cliente)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
