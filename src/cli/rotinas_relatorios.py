# Rotinas de interface para geração de relatórios CSV.
# Delega a montagem dos dados ao módulo relatorios.py e a escrita ao arquivos.py.

import os

import services.arquivos as arquivos
from db.database import ErroRepositorio
from db.repositorio_insumo import InsumoRepositorio
from db.repositorio_movimentacao import MovimentacaoRepositorio
from services.relatorios import montar_critico, montar_estoque, montar_movimentacoes
from cli.escritor import aguardar, exibir_cabecalho, limpar_tela

# Relatórios são salvos em document/other/ conforme template FIAP
_DOCUMENT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'document', 'other'
)


def rotina_relatorio_estoque(repo_insumo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('RELATÓRIO: ESTOQUE ATUAL (.csv)')

    try:
        insumos = repo_insumo.listar()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if not insumos:
        print('  Nenhum insumo para exportar.')
        aguardar()
        return

    caminho = os.path.join(_DOCUMENT, 'relatorio_estoque.csv')
    if arquivos.gerar_csv(montar_estoque(insumos), caminho):
        print(f'  Relatório gerado: document/other/relatorio_estoque.csv ({len(insumos)} insumos)')
        arquivos.gravar_log(f'RELATORIO ESTOQUE: {len(insumos)} registros em {caminho}')
    aguardar()


def rotina_relatorio_critico(repo_insumo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('RELATÓRIO: ESTOQUE CRÍTICO (.csv)')

    try:
        insumos = repo_insumo.listar()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    dados = montar_critico(insumos)
    if not dados:
        print('  Nenhum insumo em estoque crítico.')
        aguardar()
        return

    caminho = os.path.join(_DOCUMENT, 'relatorio_critico.csv')
    if arquivos.gerar_csv(dados, caminho):
        print(f'  Relatório gerado: document/other/relatorio_critico.csv ({len(dados)} itens críticos)')
        arquivos.gravar_log(f'RELATORIO CRITICO: {len(dados)} registros em {caminho}')
    aguardar()


def rotina_relatorio_movimentacoes(repo_mov: MovimentacaoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('RELATÓRIO: MOVIMENTAÇÕES (.csv)')

    try:
        movs = repo_mov.listar()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if not movs:
        print('  Nenhuma movimentação registrada.')
        aguardar()
        return

    caminho = os.path.join(_DOCUMENT, 'relatorio_movimentacoes.csv')
    if arquivos.gerar_csv(montar_movimentacoes(movs), caminho):
        print(f'  Relatório gerado: document/other/relatorio_movimentacoes.csv ({len(movs)} movimentações)')
        arquivos.gravar_log(f'RELATORIO MOVIMENTACOES: {len(movs)} registros em {caminho}')
    aguardar()
