# Rotinas de interface para exportação/importação JSON e exibição de log.

import os
import services.arquivos as arquivos
from db.database import ErroRepositorio
from db.repositorio_insumo import InsumoRepositorio
from services.insumo import UNIDADES, validar_categoria, validar_unidade
from cli.escritor import aguardar, exibir_cabecalho, limpar_tela

# Exportações ficam em document/other/ junto com os relatórios CSV
_DOCUMENT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'document', 'other'
)
ARQUIVO_EXPORT = os.path.join(_DOCUMENT, 'insumos_export.json')


def rotina_exportar(repo_insumo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('EXPORTAR INSUMOS PARA JSON')

    try:
        insumos = repo_insumo.listar()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if not insumos:
        print('  Nenhum dado para exportar.')
        aguardar()
        return

    serializaveis = []
    for r in insumos:
        item = dict(r)
        if hasattr(item.get('data_cadastro'), 'strftime'):
            item['data_cadastro'] = item['data_cadastro'].strftime('%Y-%m-%d')
        serializaveis.append(item)

    os.makedirs(_DOCUMENT, exist_ok=True)
    if arquivos.exportar_json(serializaveis, ARQUIVO_EXPORT):
        print(f'  {len(insumos)} insumo(s) exportado(s) para "document/other/insumos_export.json".')
        arquivos.gravar_log(f'EXPORTACAO JSON: {len(insumos)} insumos em {ARQUIVO_EXPORT}')
    aguardar()


def rotina_importar(repo_insumo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('IMPORTAR INSUMOS DE JSON')

    caminho = input(f'  Arquivo JSON [document/other/insumos_export.json]: ').strip() or ARQUIVO_EXPORT
    dados = arquivos.importar_json(caminho)
    if dados is None:
        aguardar()
        return

    campos_obrigatorios = ('nome', 'categoria', 'unidade', 'quantidade',
                           'estoque_min', 'preco_unit')
    importados = erros = 0

    for item in dados:
        try:
            if not all(c in item for c in campos_obrigatorios):
                erros += 1
                continue
            categoria = str(item['categoria']).upper()
            if not validar_categoria(categoria):
                erros += 1
                continue
            # Canonicaliza para o valor exato do tuple (ex: 'l' → 'L')
            unidade = next((u for u in UNIDADES if u.lower() == str(item['unidade']).lower()), None)
            if unidade is None:
                erros += 1
                continue
            repo_insumo.cadastrar(
                nome        = str(item['nome']),
                categoria   = categoria,
                unidade     = unidade,
                quantidade  = float(item['quantidade']),
                estoque_min = float(item['estoque_min']),
                preco_unit  = float(item['preco_unit']),
                fornecedor  = str(item.get('fornecedor', '') or ''),
            )
            importados += 1
        except (KeyError, ValueError, TypeError, ErroRepositorio) as e:
            print(f'  AVISO: item ignorado — {type(e).__name__}: {e}')
            erros += 1

    print(f'\n  Importados: {importados} | Erros: {erros}')
    arquivos.gravar_log(
        f'IMPORTACAO JSON: {importados} insumos importados de {caminho}, {erros} erro(s).'
    )
    aguardar()


def rotina_log() -> None:
    limpar_tela()
    exibir_cabecalho('LOG DO SISTEMA')
    arquivos.exibir_log()
    aguardar()
