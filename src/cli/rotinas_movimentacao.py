# Rotinas de interface para registro e listagem de movimentações de estoque.

import services.arquivos as arquivos
from db.database import ErroRepositorio
from db.repositorio_insumo import InsumoRepositorio
from db.repositorio_movimentacao import MovimentacaoRepositorio
from services.movimentacao import TIPOS_MOV
from services.relatorios import montar_estoque, montar_movimentacoes
from cli.escritor import (
    aguardar,
    exibir_cabecalho,
    exibir_dataframe,
    ler_id,
    ler_numero_positivo,
    ler_opcao,
    limpar_tela,
)


def rotina_movimentacao(repo_insumo: InsumoRepositorio,
                        repo_mov: MovimentacaoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('REGISTRAR MOVIMENTAÇÃO')

    try:
        insumos = repo_insumo.listar()
        if not insumos:
            print('  Nenhum insumo cadastrado.')
            aguardar()
            return

        exibir_dataframe(montar_estoque(insumos))

        insumo_id = ler_id('\n  ID do insumo')
        if insumo_id is None:
            aguardar()
            return

        insumo = repo_insumo.buscar_por_id(insumo_id)
        if insumo is None:
            print(f'  Insumo ID {insumo_id} não encontrado.')
            aguardar()
            return

        tipo = ler_opcao(TIPOS_MOV, 'Tipo de movimentação')
        if tipo is None:
            aguardar()
            return

        quantidade = ler_numero_positivo(f'  Quantidade ({insumo["unidade"]}): ', 'Quantidade')

        motivo = input('  Motivo (opcional — ENTER para pular): ').strip()

        repo_mov.registrar(insumo_id, tipo, quantidade, motivo)

    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return
    else:
        # else: executado apenas quando nenhuma exceção ocorre no try
        print(f'\n  Movimentação registrada! {tipo}: {quantidade} {insumo["unidade"]}')
        arquivos.gravar_log(
            f'MOVIMENTACAO: insumo_id={insumo_id}, nome={insumo["nome"]}, '
            f'tipo={tipo}, qtd={quantidade}, motivo={motivo or "-"}'
        )
    aguardar()


def rotina_listar_movimentacoes(repo_insumo: InsumoRepositorio,
                                repo_mov: MovimentacaoRepositorio) -> None:
    limpar_tela()
    exibir_cabecalho('LISTAGEM DE MOVIMENTAÇÕES')

    try:
        insumos = repo_insumo.listar()
        if not insumos:
            print('  Nenhum insumo cadastrado.')
            aguardar()
            return

        exibir_dataframe(montar_estoque(insumos))

        entrada = input('\n  Filtrar por ID do insumo (ENTER = todas, 0 = cancelar): ').strip()
        if entrada == '0':
            print('  Operação cancelada.')
            aguardar()
            return
        try:
            insumo_id: int | None = int(entrada) if entrada else None
        except ValueError:
            insumo_id = None

        movs = repo_mov.listar(insumo_id)

    except ErroRepositorio as e:
        print(f'  ERRO: {e}')
        aguardar()
        return

    if not movs:
        print('  Nenhuma movimentação encontrada.')
        aguardar()
        return

    exibir_dataframe(montar_movimentacoes(movs))
    print(f'\n  Total: {len(movs)} movimentação(ões)')
    aguardar()
