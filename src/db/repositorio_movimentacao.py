# Repositório de acesso à tabela movimentacao.
# Centraliza todo SQL de movimentações, incluindo a transação atômica de estoque.

import oracledb

from db.database import ErroRepositorio

_COLUNAS = (
    'id', 'insumo_id', 'nome_insumo', 'categoria',
    'tipo', 'quantidade', 'unidade', 'motivo', 'data_mov',
)


class MovimentacaoRepositorio:
    """Operações na tabela movimentacao. Recebe conexão por injeção (DIP)."""

    def __init__(self, conn: oracledb.Connection) -> None:
        self._conn = conn

    # ── CREATE (atômico) ────────────────────────────────────────────────────────

    def registrar(self, insumo_id: int, tipo: str,
                  quantidade: float, motivo: str) -> None:
        """
        Registra entrada ou saída de estoque de forma atômica:
          1. Bloqueia a linha do insumo (SELECT FOR UPDATE)
          2. Valida estoque suficiente para SAIDA
          3. Atualiza insumo.quantidade
          4. Insere registro em movimentacao
          5. Commit único — rollback em caso de erro
        """
        sql_lock   = 'SELECT quantidade FROM insumo WHERE id = :1 FOR UPDATE'
        sql_update = 'UPDATE insumo SET quantidade = :1 WHERE id = :2'
        sql_insert = """
            INSERT INTO movimentacao (insumo_id, tipo, quantidade, motivo)
            VALUES (:1, :2, :3, :4)
        """
        try:
            with self._conn.cursor() as cur:
                cur.execute(sql_lock, (insumo_id,))
                linha = cur.fetchone()
                if linha is None:
                    raise ErroRepositorio(f'Insumo ID {insumo_id} não encontrado.')

                qtd_atual = float(linha[0])
                if tipo == 'SAIDA' and quantidade > qtd_atual:
                    raise ErroRepositorio(
                        f'Estoque insuficiente. '
                        f'Disponível: {qtd_atual:.3f} | Solicitado: {quantidade:.3f}'
                    )

                nova_qtd = qtd_atual + quantidade if tipo == 'ENTRADA' else qtd_atual - quantidade
                cur.execute(sql_update, (nova_qtd, insumo_id))
                cur.execute(sql_insert, (insumo_id, tipo, quantidade, motivo or ''))

            self._conn.commit()

        except ErroRepositorio:
            raise
        except oracledb.DatabaseError as e:
            self._conn.rollback()
            raise ErroRepositorio(f'Erro ao registrar movimentação: {e}') from e

    def excluir_por_insumo(self, insumo_id: int) -> None:
        """Remove todas as movimentações de um insumo (chamado antes de excluir o insumo)."""
        try:
            with self._conn.cursor() as cur:
                cur.execute('DELETE FROM movimentacao WHERE insumo_id = :1', (insumo_id,))
                self._conn.commit()
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao excluir movimentações do insumo: {e}') from e

    def excluir_todas(self) -> None:
        """Remove todas as movimentações (chamado antes de excluir todos os insumos)."""
        try:
            with self._conn.cursor() as cur:
                cur.execute('DELETE FROM movimentacao')
                self._conn.commit()
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao excluir todas as movimentações: {e}') from e

    # ── READ ───────────────────────────────────────────────────────────────────

    def listar(self, insumo_id: int | None = None) -> list[dict]:
        """
        Retorna movimentações com JOIN em insumo para exibir nome e categoria.
        Filtra por insumo_id se informado.
        """
        sql = """
            SELECT m.id, m.insumo_id, i.nome, i.categoria,
                   m.tipo, m.quantidade, i.unidade, m.motivo, m.data_mov
              FROM movimentacao m
              JOIN insumo i ON i.id = m.insumo_id
        """
        params: tuple = ()
        if insumo_id is not None:
            sql += ' WHERE m.insumo_id = :1'
            params = (insumo_id,)
        sql += ' ORDER BY m.data_mov DESC'

        try:
            with self._conn.cursor() as cur:
                cur.execute(sql, params)
                return [dict(zip(_COLUNAS, row)) for row in cur.fetchall()]
        except oracledb.DatabaseError as e:
            raise ErroRepositorio(f'Erro ao listar movimentações: {e}') from e
