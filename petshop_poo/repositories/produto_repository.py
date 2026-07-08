"""
repositories/produto_repository.py
Acesso ao banco para a entidade Produto.
"""

import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.produto import Produto
from models.excecoes import RegistroVinculadoError
from repositories.base_repository import RepositorioBase


class ProdutoRepository(RepositorioBase):
    def criar(self, produto: Produto) -> Produto:
        sql = """
            INSERT INTO Produto (Nome, Preco, Estoque)
            VALUES (%s, %s, %s)
            RETURNING Id_produto, Nome, Preco, Estoque;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (produto.nome, produto.preco, produto.estoque))
                row = cur.fetchone()
            conn.commit()
            return Produto.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def listar(self):
        sql = "SELECT Id_produto, Nome, Preco, Estoque FROM Produto ORDER BY Nome;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Produto.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def buscar_por_id(self, id_produto):
        sql = "SELECT Id_produto, Nome, Preco, Estoque FROM Produto WHERE Id_produto = %s;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_produto,))
                row = cur.fetchone()
                return Produto.from_dict(row) if row else None
        finally:
            conn.close()

    def atualizar(self, id_produto, nome=None, preco=None, estoque=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("Nome = %s")
            valores.append(nome)
        if preco is not None:
            campos.append("Preco = %s")
            valores.append(preco)
        if estoque is not None:
            campos.append("Estoque = %s")
            valores.append(estoque)

        if not campos:
            return self.buscar_por_id(id_produto)

        sql = f"""
            UPDATE Produto SET {', '.join(campos)}
            WHERE Id_produto = %s
            RETURNING Id_produto, Nome, Preco, Estoque;
        """
        valores.append(id_produto)

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, valores)
                row = cur.fetchone()
            conn.commit()
            return Produto.from_dict(row) if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def deletar(self, id_produto):
        sql = "DELETE FROM Produto WHERE Id_produto = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_produto,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            raise RegistroVinculadoError("Produto", id_produto)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
