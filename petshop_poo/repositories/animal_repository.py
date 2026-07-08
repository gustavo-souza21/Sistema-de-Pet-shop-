"""
repositories/animal_repository.py
Acesso ao banco para a entidade Animal.
"""

import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.animal import Animal
from models.excecoes import RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class AnimalRepository(RepositorioBase):
    def criar(self, animal: Animal) -> Animal:
        sql = """
            INSERT INTO Animal (Nome, Especie, Data_nascimento, Id_cliente)
            VALUES (%s, %s, %s, %s)
            RETURNING Cod_animal, Nome, Especie, Data_nascimento, Id_cliente;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (animal.nome, animal.especie, animal.data_nascimento, animal.id_cliente))
                row = cur.fetchone()
            conn.commit()
            return Animal.from_dict(row)
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        sql = """
            SELECT
                a.Cod_animal, a.Nome, a.Especie, a.Data_nascimento,
                a.Id_cliente, c.Nome AS nome_tutor
            FROM Animal a
            JOIN Cliente c ON c.Cod_cliente = a.Id_cliente
            ORDER BY a.Nome;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Animal.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def listar_por_cliente(self, id_cliente):
        sql = """
            SELECT Cod_animal, Nome, Especie, Data_nascimento, Id_cliente
            FROM Animal
            WHERE Id_cliente = %s
            ORDER BY Nome;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_cliente,))
                return [Animal.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, cod_animal):
        sql = """
            SELECT Cod_animal, Nome, Especie, Data_nascimento, Id_cliente
            FROM Animal WHERE Cod_animal = %s;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (cod_animal,))
                row = cur.fetchone()
                return Animal.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, cod_animal, nome=None, especie=None, data_nascimento=None, id_cliente=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("Nome = %s")
            valores.append(nome)
        if especie is not None:
            campos.append("Especie = %s")
            valores.append(especie)
        if data_nascimento is not None:
            campos.append("Data_nascimento = %s")
            valores.append(data_nascimento)
        if id_cliente is not None:
            campos.append("Id_cliente = %s")
            valores.append(id_cliente)

        if not campos:
            return self.buscar_por_id(cod_animal)

        sql = f"""
            UPDATE Animal SET {', '.join(campos)}
            WHERE Cod_animal = %s
            RETURNING Cod_animal, Nome, Especie, Data_nascimento, Id_cliente;
        """
        valores.append(cod_animal)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Animal.from_dict(row) if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, cod_animal):
        sql = "DELETE FROM Animal WHERE Cod_animal = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (cod_animal,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Animal", cod_animal)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
