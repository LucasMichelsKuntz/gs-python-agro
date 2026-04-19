"""
Script de seed: popula o banco com dados de amostra de insumos e movimentações.
Execute a partir da raiz do projeto:
    python scripts/seed.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import config
from db import database
from db.repositorio_insumo import InsumoRepositorio
from db.repositorio_movimentacao import MovimentacaoRepositorio

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
INSUMOS_JSON      = ASSETS / 'insumos_amostra.json'
MOVIMENTACOES_JSON = ASSETS / 'movimentacoes_amostra.json'


def main() -> None:
    try:
        config.validar()
    except EnvironmentError as e:
        print(f'ERRO de configuração: {e}')
        sys.exit(1)

    try:
        conn = database.conectar()
    except database.ErroRepositorio as e:
        print(f'ERRO de conexão: {e}')
        sys.exit(1)

    database.criar_tabelas(conn)
    repo_insumo = InsumoRepositorio(conn)
    repo_mov    = MovimentacaoRepositorio(conn)

    # ── importar insumos ───────────────────────────────────────────────────────
    insumos_raw = json.loads(INSUMOS_JSON.read_text(encoding='utf-8'))
    print(f'\nImportando {len(insumos_raw)} insumos...')
    for item in insumos_raw:
        try:
            repo_insumo.cadastrar(
                nome        = item['nome'],
                categoria   = item['categoria'].upper(),
                unidade     = item['unidade'].lower(),
                quantidade  = float(item['quantidade']),
                estoque_min = float(item['estoque_min']),
                preco_unit  = float(item['preco_unit']),
                fornecedor  = item.get('fornecedor', ''),
            )
            print(f'  OK  {item["nome"]}')
        except Exception as e:
            print(f'  ERR {item["nome"]}: {e}')

    # ── resolver nome → id ─────────────────────────────────────────────────────
    todos = repo_insumo.listar()
    nome_para_id = {r['nome']: r['id'] for r in todos}

    # ── importar movimentações ─────────────────────────────────────────────────
    movs_raw = json.loads(MOVIMENTACOES_JSON.read_text(encoding='utf-8'))
    print(f'\nImportando {len(movs_raw)} movimentações...')
    for mov in movs_raw:
        nome = mov['insumo_nome']
        insumo_id = nome_para_id.get(nome)
        if insumo_id is None:
            print(f'  ERR Insumo não encontrado: "{nome}"')
            continue
        try:
            repo_mov.registrar(
                insumo_id = insumo_id,
                tipo      = mov['tipo'].upper(),
                quantidade = float(mov['quantidade']),
                motivo    = mov.get('motivo', ''),
            )
            print(f'  OK  {mov["tipo"]:7s} {mov["quantidade"]:>8.1f}  →  {nome}')
        except Exception as e:
            print(f'  ERR {nome}: {e}')

    conn.close()
    print('\nSeed concluído.')


if __name__ == '__main__':
    main()
