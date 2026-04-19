# Repositório de acesso à tabela insumo.
# Encapsula todo SQL da entidade insumo — nenhum outro módulo acessa esta tabela diretamente.

import oracledb

from db.database import ErroRepositorio

_COLUNAS = (
    'id', 'nome', 'categoria', 'unidade',
    'quantidade', 'estoque_min', 'preco_unit', 'fornecedor', 'data_cadastro',
)


class InsumoRepositorio:
    """CRUD da tabela insumo. Recebe conexão por injeção (DIP)."""

    def __init__(self, conn: oracledb.Connection) -> None:
        self._conn = conn

    def cadastrar(self, nome: str, categoria: str, unidade: str,
                  quantidade: float, estoque_min: float,
                  preco_unit: float, fornecedor: str) -> None:
        sql = """
            INSERT INTO insumo (nome, categoria, unidade, quantidade, estoque_min, preco_unit, fornecedor)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, (nome, categoria, unidade, quantidade, estoque_min, preco_unit, fornecedor or None))
                self._conn.commit()
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao cadastrar insumo: {e}') from e

    def listar(self) -> list[dict]:
        """Retorna todos os insumos ordenados por categoria e nome."""
        sql = """
            SELECT id, nome, categoria, unidade, quantidade, estoque_min,
                   preco_unit, fornecedor, data_cadastro
              FROM insumo
             ORDER BY categoria, nome
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql)
                return [dict(zip(_COLUNAS, row)) for row in cur.fetchall()]
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao listar insumos: {e}') from e

    def buscar_por_id(self, id_insumo: int) -> dict | None:
        sql = """
            SELECT id, nome, categoria, unidade, quantidade, estoque_min,
                   preco_unit, fornecedor, data_cadastro
              FROM insumo WHERE id = :1
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, (id_insumo,))
                linha = cur.fetchone()
                return dict(zip(_COLUNAS, linha)) if linha else None
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao buscar insumo: {e}') from e

    def alterar(self, id_insumo: int, nome: str, categoria: str,
                unidade: str, estoque_min: float,
                preco_unit: float, fornecedor: str) -> bool:
        """
        Atualiza campos cadastrais do insumo.
        A quantidade é gerenciada exclusivamente pelo MovimentacaoRepositorio.
        Retorna True se o registro foi encontrado e alterado.
        """
        sql = """
            UPDATE insumo
               SET nome = :1, categoria = :2, unidade = :3,
                   estoque_min = :4, preco_unit = :5, fornecedor = :6
             WHERE id = :7
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, (nome, categoria, unidade, estoque_min,
                                  preco_unit, fornecedor or None, id_insumo))
                self._conn.commit()
                return cur.rowcount > 0
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao alterar insumo: {e}') from e

    def excluir(self, id_insumo: int) -> bool:
        """Remove o insumo. Movimentações devem ser excluídas antes (respeitar FK)."""
        try:
            with self._conn.cursor() as cur:
                cur.execute('DELETE FROM insumo WHERE id = :1', (id_insumo,))
                self._conn.commit()
                return cur.rowcount > 0
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao excluir insumo: {e}') from e

    def excluir_todos(self) -> int:
        """Remove todos os insumos. Movimentações devem ser excluídas antes."""
        try:
            with self._conn.cursor() as cur:
                cur.execute('DELETE FROM insumo')
                self._conn.commit()
                return cur.rowcount
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao excluir todos os insumos: {e}') from e
