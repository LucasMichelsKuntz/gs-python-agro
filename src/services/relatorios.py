# Módulo de relatórios: monta listas de dicionários prontas para CSV ou exibição.
# Sem I/O e sem acesso a banco — recebe dados já carregados e retorna estruturas.

from services.insumo import calcular_valor_estoque, esta_em_estoque_critico


def montar_estoque(insumos: list[dict]) -> list[dict]:
    """
    Retorna tabela enriquecida de todos os insumos.
    Adiciona 'Valor Total' e 'Status' calculados a partir dos dados brutos.
    """
    tabela = []
    for r in insumos:
        valor = calcular_valor_estoque(r['quantidade'], r['preco_unit'])
        critico = esta_em_estoque_critico(r['quantidade'], r['estoque_min'])
        tabela.append({
            'ID':          r['id'],
            'Nome':        r['nome'],
            'Categoria':   r['categoria'],
            'Unid.':       r['unidade'],
            'Qtd':         r['quantidade'],
            'Est.Min':     r['estoque_min'],
            'R$/un':       r['preco_unit'],
            'Valor Total': valor,
            'Fornecedor':  r['fornecedor'] or '',
            'Status':      'CRITICO (!)' if critico else 'OK',
        })
    return tabela


def montar_critico(insumos: list[dict]) -> list[dict]:
    """Filtra insumos em estoque crítico e retorna tabela enriquecida."""
    criticos = [r for r in insumos if esta_em_estoque_critico(r['quantidade'], r['estoque_min'])]
    return montar_estoque(criticos)


def montar_movimentacoes(movs: list[dict]) -> list[dict]:
    """
    Retorna tabela de movimentações com colunas legíveis para CSV e terminal.
    Converte datas para string para garantir serialização correta.
    """
    dados = []
    for m in movs:
        data = m['data_mov']
        if hasattr(data, 'strftime'):
            data = data.strftime('%Y-%m-%d %H:%M:%S')
        dados.append({
            'ID':        m['id'],
            'Insumo':    m['nome_insumo'],
            'Categoria': m['categoria'],
            'Tipo':      m['tipo'],
            'Qtd':       m['quantidade'],
            'Unid.':     m['unidade'],
            'Motivo':    m['motivo'] or '',
            'Data':      data,
        })
    return dados
