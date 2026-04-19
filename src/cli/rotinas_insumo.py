# Rotinas de interface para o CRUD de insumos.

import services.arquivos as arquivos
from db.database import ErroRepositorio
from db.repositorio_insumo import InsumoRepositorio
from db.repositorio_movimentacao import MovimentacaoRepositorio
from services.insumo import (
    CATEGORIAS,
    UNIDADES,
    esta_em_estoque_critico,
    validar_numero_positivo,
)
from services.relatorios import montar_estoque
from cli.escritor import (
    aguardar,
    exibir_cabecalho,
    exibir_dataframe,
    ler_id,
    ler_numero_nao_negativo,
    ler_numero_positivo,
    ler_opcao,
    limpar_tela,
)


def _ler_numero_editavel(label: str, atual: float) -> float | None:
    """
    Lê campo numérico positivo editável em loop.
    ENTER mantém o atual. '0' cancela (retorna None). Inválido repete.
    """
    while True:
        txt = input(f'  {label} [{atual}]: ').strip()
        if txt == '0':
            print('  Operação cancelada.')
            return None
        if not txt:
            return atual
        val = validar_numero_positivo(txt, label)
        if val is not None:
            return val


def rotina_cadastrar(repo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('CADASTRAR INSUMO')
    print('  (Digite 0 para cancelar a qualquer momento)\n')

    while True:
        nome = input('  Nome do insumo: ').strip()
        if nome == '0':
            print('  Operação cancelada.')
            aguardar()
            return
        if nome:
            break
        print('  ERRO: Nome não pode ser vazio. Tente novamente.')

    categoria = ler_opcao(CATEGORIAS, 'Categoria')
    if categoria is None:
        aguardar()
        return

    unidade = ler_opcao(UNIDADES, 'Unidade')
    if unidade is None:
        aguardar()
        return

    quantidade  = ler_numero_nao_negativo('  Quantidade inicial: ', 'Quantidade')
    estoque_min = ler_numero_positivo('  Estoque mínimo: ', 'Estoque mínimo')
    preco_unit  = ler_numero_positivo('  Preço unitário (R$): ', 'Preço unitário')
    fornecedor  = input('  Fornecedor (opcional — ENTER para pular): ').strip()

    try:
        repo.cadastrar(nome, categoria, unidade, quantidade,
                       estoque_min, preco_unit, fornecedor)
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return
    else:
        # else: executado apenas quando nenhuma exceção ocorre no try
        print(f'\n  Insumo "{nome}" cadastrado com sucesso!')
        arquivos.gravar_log(
            f'CADASTRO INSUMO: nome={nome}, categoria={categoria}, '
            f'unidade={unidade}, qtd={quantidade}, preco={preco_unit}'
        )
    aguardar()


def rotina_listar(repo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('LISTAGEM DE INSUMOS')

    try:
        insumos = repo.listar()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if not insumos:
        print('  Nenhum insumo cadastrado.')
        aguardar()
        return

    exibir_dataframe(montar_estoque(insumos))

    criticos = sum(1 for r in insumos if esta_em_estoque_critico(r['quantidade'], r['estoque_min']))
    print(f'\n  Total: {len(insumos)} insumo(s) | Em estoque crítico: {criticos}')
    if criticos:
        print('  CRITICO (!) = quantidade abaixo do estoque mínimo.')
    aguardar()


def rotina_alterar(repo: InsumoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('ALTERAR INSUMO')

    insumo_id = ler_id('  ID do insumo a alterar')
    if insumo_id is None:
        aguardar()
        return

    try:
        insumo = repo.buscar_por_id(insumo_id)
        if insumo is None:
            print(f'  Insumo ID {insumo_id} não encontrado.')
            aguardar()
            return

        print('\n  Dados atuais:')
        exibir_dataframe(montar_estoque([insumo]))
        print('  (ENTER = manter valor atual | 0 = cancelar)\n')

        while True:
            nome = input(f'  Nome [{insumo["nome"]}]: ').strip()
            if nome == '0':
                print('  Operação cancelada.')
                aguardar()
                return
            nome = nome or insumo['nome']
            break

        categoria = ler_opcao(CATEGORIAS, 'Categoria', atual=insumo['categoria'])
        if categoria is None:
            aguardar()
            return

        unidade = ler_opcao(UNIDADES, 'Unidade', atual=insumo['unidade'])
        if unidade is None:
            aguardar()
            return

        estoque_min = _ler_numero_editavel('Estoque mínimo', insumo['estoque_min'])
        if estoque_min is None:
            aguardar()
            return

        preco_unit = _ler_numero_editavel('Preço unitário', insumo['preco_unit'])
        if preco_unit is None:
            aguardar()
            return

        forn_input = input(f'  Fornecedor [{insumo["fornecedor"] or ""}]: ').strip()
        fornecedor = forn_input if forn_input else (insumo['fornecedor'] or '')

        atualizado = repo.alterar(insumo_id, nome, categoria, unidade,
                                  estoque_min, preco_unit, fornecedor)

    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if atualizado:
        print(f'\n  Insumo ID {insumo_id} atualizado com sucesso!')
        arquivos.gravar_log(f'ALTERACAO INSUMO: ID={insumo_id}, nome={nome}')
    else:
        print('  Nenhum registro foi alterado.')
    aguardar()


def rotina_excluir(repo_insumo: InsumoRepositorio,
                   repo_mov: MovimentacaoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('EXCLUIR INSUMO')

    insumo_id = ler_id('  ID do insumo a excluir')
    if insumo_id is None:
        aguardar()
        return

    try:
        insumo = repo_insumo.buscar_por_id(insumo_id)
        if insumo is None:
            print(f'  Insumo ID {insumo_id} não encontrado.')
            aguardar()
            return

        print('\n  Insumo a excluir (e todas as suas movimentações):')
        exibir_dataframe(montar_estoque([insumo]))

        if input('\n  Confirma exclusão? (S/N): ').strip().upper() != 'S':
            print('  Operação cancelada.')
            aguardar()
            return

        repo_mov.excluir_por_insumo(insumo_id)
        removido = repo_insumo.excluir(insumo_id)

    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if removido:
        print(f'  Insumo ID {insumo_id} excluído.')
        arquivos.gravar_log(f'EXCLUSAO INSUMO: ID={insumo_id}, nome={insumo["nome"]}')
    else:
        print('  Insumo não foi excluído.')
    aguardar()


def rotina_excluir_todos(repo_insumo: InsumoRepositorio,
                         repo_mov: MovimentacaoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('EXCLUIR TODOS OS INSUMOS')
    print('  ATENÇÃO: Esta operação remove todos os insumos e movimentações permanentemente.')

    if input('  Confirma? (S/N): ').strip().upper() != 'S':
        print('  Operação cancelada.')
        aguardar()
        return

    try:
        repo_mov.excluir_todas()
        removidos = repo_insumo.excluir_todos()
    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    print(f'  {removidos} insumo(s) removido(s).')
    arquivos.gravar_log(f'EXCLUSAO TOTAL: {removidos} insumos removidos.')
    aguardar()
