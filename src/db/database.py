# Infraestrutura de banco: exceção tipada, fábrica de conexão e criação de tabelas.
# Os repositórios específicos vivem em db/repositorio_insumo.py e db/repositorio_movimentacao.py.

import oracledb

import config

# ─── DDL ──────────────────────────────────────────────────────────────────────

_SQL_CRIAR_INSUMO = """
    CREATE TABLE insumo (
        id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nome          VARCHAR2(60)  NOT NULL,
        categoria     VARCHAR2(20)  NOT NULL,
        unidade       VARCHAR2(5)   NOT NULL,
        quantidade    NUMBER(12, 3) NOT NULL,
        estoque_min   NUMBER(12, 3) NOT NULL,
        preco_unit    NUMBER(10, 2) NOT NULL,
        fornecedor    VARCHAR2(60),
        data_cadastro DATE DEFAULT SYSDATE NOT NULL,
        CONSTRAINT chk_insumo_categoria CHECK (
            categoria IN ('SEMENTE','FERTILIZANTE','DEFENSIVO','CORRETIVO','COMBUSTIVEL','OUTRO')
        ),
        CONSTRAINT chk_insumo_unidade CHECK (
            unidade IN ('kg','L','un','sc','t')
        )
    )
"""

_SQL_CRIAR_MOVIMENTACAO = """
    CREATE TABLE movimentacao (
        id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        insumo_id  NUMBER        NOT NULL,
        tipo       VARCHAR2(10)  NOT NULL,
        quantidade NUMBER(12, 3) NOT NULL,
        motivo     VARCHAR2(100),
        data_mov   DATE DEFAULT SYSDATE NOT NULL,
        CONSTRAINT chk_mov_tipo  CHECK (tipo IN ('ENTRADA','SAIDA')),
        CONSTRAINT fk_mov_insumo FOREIGN KEY (insumo_id) REFERENCES insumo(id)
    )
"""


class ErroRepositorio(Exception):
    """Exceção tipada para falhas de banco — isola oracledb do restante da aplicação."""


def conectar() -> oracledb.Connection:
    """Abre e retorna uma conexão Oracle configurada via .env."""
    try:
        return oracledb.connect(
            user=config.DB_USUARIO,
            password=config.DB_SENHA,
            dsn=config.DB_DSN,
        )
    except oracledb.DatabaseError as e:
        raise ErroRepositorio(f'Falha na conexão com o Oracle: {e}') from e


def criar_tabelas(conn: oracledb.Connection) -> None:
    """Cria as tabelas insumo e movimentacao se ainda não existirem."""
    for sql in (_SQL_CRIAR_INSUMO, _SQL_CRIAR_MOVIMENTACAO):
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
        except oracledb.DatabaseError as e:
            if 'ORA-00955' not in str(e):
                raise ErroRepositorio(f'Erro ao criar tabela: {e}') from e
