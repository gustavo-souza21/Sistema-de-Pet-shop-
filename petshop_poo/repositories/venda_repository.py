"""
repositories/venda_repository.py
Acesso ao banco para Venda, Item_venda (servicos baixados) e
Intem_Produto (produtos vendidos).

PONTO CRITICO DE DESIGN: Venda.Valor e calculado automaticamente por uma
trigger no PostgreSQL (fn_recalcula_valor_venda), toda vez que uma linha
e inserida/atualizada/deletada em Item_venda ou Intem_Produto. As funcoes
abaixo NUNCA escrevem em Venda.Valor diretamente.
"""

import psycopg2

from database.connection import get_connection, get_dict_cursor
from models.venda import Venda, ItemServico, ItemProduto
from repositories.base_repository import RepositorioBase


class VendaRepository(RepositorioBase):
    # -- Venda ------------------------------------------------------------------
    def criar(self, venda: Venda) -> Venda:
        """Cria uma venda vazia (Valor comeca em 0, conforme DEFAULT do banco)."""
        sql = """
            INSERT INTO Venda (Id_cliente, Id_agendamento)
            VALUES (%s, %s)
            RETURNING Id_venda, Data, Valor, Id_cliente, Id_agendamento;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (venda.id_cliente, venda.id_agendamento))
                row = cur.fetchone()
            conn.commit()
            return Venda.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def buscar_por_id(self, id_venda):
        sql = "SELECT Id_venda, Data, Valor, Id_cliente, Id_agendamento FROM Venda WHERE Id_venda = %s;"
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_venda,))
                row = cur.fetchone()
                return Venda.from_dict(row) if row else None
        finally:
            conn.close()

    def listar(self):
        sql = """
            SELECT v.Id_venda, v.Data, v.Valor, v.Id_cliente, c.Nome AS nome_cliente, v.Id_agendamento
            FROM Venda v
            LEFT JOIN Cliente c ON c.Cod_cliente = v.Id_cliente
            ORDER BY v.Data DESC, v.Id_venda DESC;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql)
                return [Venda.from_dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def detalhar(self, id_venda):
        """Retorna a Venda com os objetos ItemServico/ItemProduto ja carregados."""
        venda = self.buscar_por_id(id_venda)
        if venda is None:
            return None

        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute("""
                    SELECT iv.Id_item_venda, iv.Id_agendamento, s.Tipo_servico,
                           iv.Quantidade, iv.Valor_unitario
                    FROM Item_venda iv
                    JOIN Agendamento ag ON ag.Id_agendamento = iv.Id_agendamento
                    JOIN Servico s ON s.Id_servico = ag.Id_servico
                    WHERE iv.Id_venda = %s;
                """, (id_venda,))
                for row in cur.fetchall():
                    venda.adicionar_item(ItemServico.from_dict(row))

                cur.execute("""
                    SELECT ip.Id_item_produto, ip.Id_produto, p.Nome AS nome_produto,
                           ip.Quantidade, ip.Valor_unitario
                    FROM Intem_Produto ip
                    JOIN Produto p ON p.Id_produto = ip.Id_produto
                    WHERE ip.Id_venda = %s;
                """, (id_venda,))
                for row in cur.fetchall():
                    venda.adicionar_item(ItemProduto.from_dict(row))
        finally:
            conn.close()

        return venda

    def atualizar(self, id_venda, **campos):
        # Venda nao tem campos livres para editar diretamente (Valor e da trigger).
        return self.buscar_por_id(id_venda)

    def deletar(self, id_venda):
        """Remove a venda. Item_venda/Intem_Produto tem ON DELETE CASCADE."""
        sql = "DELETE FROM Venda WHERE Id_venda = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_venda,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # -- Item_venda (baixa de servico) -------------------------------------------
    def adicionar_item_servico(self, id_venda, id_agendamento, valor_unitario, quantidade=1):
        sql = """
            INSERT INTO Item_venda (Id_venda, Id_agendamento, Quantidade, Valor_unitario)
            VALUES (%s, %s, %s, %s)
            RETURNING Id_item_venda, Id_venda, Id_agendamento, Quantidade, Valor_unitario;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_venda, id_agendamento, quantidade, valor_unitario))
                row = cur.fetchone()
            conn.commit()
            return ItemServico.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remover_item_servico(self, id_item_venda):
        sql = "DELETE FROM Item_venda WHERE Id_item_venda = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_item_venda,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # -- Intem_Produto (produto vendido) -----------------------------------------
    def adicionar_item_produto(self, id_venda, id_produto, valor_unitario, quantidade=1):
        sql = """
            INSERT INTO Intem_Produto (Id_venda, Id_produto, Quantidade, Valor_unitario)
            VALUES (%s, %s, %s, %s)
            RETURNING Id_item_produto, Id_venda, Id_produto, Quantidade, Valor_unitario;
        """
        conn = get_connection()
        try:
            with get_dict_cursor(conn) as cur:
                cur.execute(sql, (id_venda, id_produto, quantidade, valor_unitario))
                row = cur.fetchone()
            conn.commit()
            return ItemProduto.from_dict(row)
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def remover_item_produto(self, id_item_produto):
        sql = "DELETE FROM Intem_Produto WHERE Id_item_produto = %s;"
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (id_item_produto,))
                linhas_afetadas = cur.rowcount
            conn.commit()
            return linhas_afetadas > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
