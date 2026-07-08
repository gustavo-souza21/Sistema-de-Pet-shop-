"""
database/connection.py
Responsavel apenas por abrir e fechar conexoes com o PostgreSQL.
Nenhuma logica de negocio aqui -- so conexao.
"""

import psycopg2
import psycopg2.extras


# --------------------------------------------------------------------------
# AJUSTE ESTES DADOS PARA O SEU AMBIENTE LOCAL (o mesmo que voce usa no
# pgAdmin: usuario, senha, host, porta, nome do banco).
# --------------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "petshop",
    "user": "postgres",
    "password": "SUA_SENHA_AQUI",
}


def get_connection():
    """
    Abre e retorna uma nova conexao com o banco.
    Quem chamar esta funcao e responsavel por fechar a conexao.
    """
    return psycopg2.connect(**DB_CONFIG)


def get_dict_cursor(conn):
    """
    Retorna um cursor que devolve linhas como dicionario
    (ex: {'cod_cliente': 1, 'nome': 'Maria'}) em vez de tupla posicional.
    """
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
