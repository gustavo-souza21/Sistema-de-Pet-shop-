import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.funcionario import Funcionario
from models.excecoes import CpfDuplicadoError, RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class FuncionarioRepository(RepositorioBase):
    def criar(self, funcionario: Funcionario) -> Funcionario:
        sql = """
            INSERT INTO Funcionario (Nome, Cpf, Cargo)
            VALUES (%s, %s, %s)
            RETURNING Id_funcionario, Nome, Cpf, Cargo;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (funcionario.nome, funcionario.cpf, funcionario.cargo))
                row = cur.fetchone()
            conn.commit()
            return Funcionario.from_dict(row)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise CpfDuplicadoError(funcionario.cpf)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        """Lista funcionarios indicando, via LEFT JOIN, veterinario e/ou tosador."""
        sql = """
            SELECT
                f.Id_funcionario, f.Nome, f.Cpf, f.Cargo,
                v.Crmv,
                t.Especialidade
            FROM Funcionario f
            LEFT JOIN Veterinario v ON v.Id_funcionario = f.Id_funcionario
            LEFT JOIN Tosador t ON t.Id_funcionario = f.Id_funcionario
            ORDER BY f.Nome;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Funcionario.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, id_funcionario):
        sql = "SELECT Id_funcionario, Nome, Cpf, Cargo FROM Funcionario WHERE Id_funcionario = %s;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_funcionario,))
                row = cur.fetchone()
                return Funcionario.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, id_funcionario, nome=None, cpf=None, cargo=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("Nome = %s")
            valores.append(nome)
        if cpf is not None:
            campos.append("Cpf = %s")
            valores.append(cpf)
        if cargo is not None:
            campos.append("Cargo = %s")
            valores.append(cargo)

        if not campos:
            return self.buscar_por_id(id_funcionario)

        sql = f"""
            UPDATE Funcionario SET {', '.join(campos)}
            WHERE Id_funcionario = %s
            RETURNING Id_funcionario, Nome, Cpf, Cargo;
        """
        valores.append(id_funcionario)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Funcionario.from_dict(row) if row else None
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise CpfDuplicadoError(cpf)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, id_funcionario):
        sql = "DELETE FROM Funcionario WHERE Id_funcionario = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_funcionario,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Funcionario", id_funcionario)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
            
    def tornar_veterinario(self, id_funcionario, crmv):
        sql = """
            INSERT INTO Veterinario (Id_funcionario, Crmv)
            VALUES (%s, %s)
            RETURNING Id_funcionario, Crmv;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_funcionario, crmv))
                row = cur.fetchone()
            conn.commit()
            return dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remover_veterinario(self, id_funcionario):
        sql = "DELETE FROM Veterinario WHERE Id_funcionario = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_funcionario,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def tornar_tosador(self, id_funcionario, especialidade=None):
        sql = """
            INSERT INTO Tosador (Id_funcionario, Especialidade)
            VALUES (%s, %s)
            RETURNING Id_funcionario, Especialidade;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_funcionario, especialidade))
                row = cur.fetchone()
            conn.commit()
            return dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remover_tosador(self, id_funcionario):
        sql = "DELETE FROM Tosador WHERE Id_funcionario = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_funcionario,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
