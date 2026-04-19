# Helpers de I/O de terminal: leitura com validação, exibição e formatação.
# Sem acesso a banco e sem lógica de negócio — apenas apresentação e leitura de input.

import os
import pandas as pd

from services.insumo import validar_numero_nao_negativo, validar_numero_positivo


def limpar_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_cabecalho(titulo: str) -> None:
    """Procedimento: imprime cabeçalho de seção formatado na tela."""
    print(f"\n{'=' * 50}")
    print(f'  {titulo}')
    print(f"{'=' * 50}")


def aguardar() -> None:
    """Pausa a execução até o usuário pressionar ENTER."""
    input('\n  [ENTER] para continuar...')


def ler_id(prompt: str) -> int | None:
    """
    Lê um ID inteiro positivo em loop até entrada válida ou cancelamento.
    Retorna None apenas quando o usuário digita 0 (cancelar).
    """
    while True:
        try:
            val = int(input(f'{prompt} (0 = cancelar): '))
            if val == 0:
                print('  Operação cancelada.')
                return None
            if val > 0:
                return val
            print('  ERRO: ID deve ser maior que zero. Tente novamente.')
        except ValueError:
            print('  ERRO: ID deve ser um número inteiro. Tente novamente.')


def ler_opcao(colecao: tuple, titulo: str, atual: str | None = None) -> str | None:
    """
    Exibe opções numeradas em loop até escolha válida ou cancelamento (0).
    Se `atual` for informado, ENTER mantém o valor atual.
    Retorna None apenas quando o usuário escolhe 0.
    """
    print(f'  {titulo}:')
    print('    0. Cancelar')
    for i, item in enumerate(colecao, start=1):
        print(f'    {i}. {item}')
    if atual is not None:
        print(f'  (ENTER = manter atual: {atual})')
    while True:
        entrada = input('  Número: ').strip()
        if atual is not None and entrada == '':
            return atual
        try:
            idx = int(entrada)
            if idx == 0:
                print('  Operação cancelada.')
                return None
            if 1 <= idx <= len(colecao):
                return colecao[idx - 1]
            print(f'  ERRO: Escolha entre 0 e {len(colecao)}. Tente novamente.')
        except ValueError:
            print('  ERRO: Digite um número. Tente novamente.')


def ler_numero_positivo(prompt: str, nome_campo: str) -> float:
    """Lê um número positivo em loop até entrada válida."""
    while True:
        val = validar_numero_positivo(input(prompt), nome_campo)
        if val is not None:
            return val


def ler_numero_nao_negativo(prompt: str, nome_campo: str) -> float:
    """Lê um número não-negativo em loop até entrada válida."""
    while True:
        val = validar_numero_nao_negativo(input(prompt), nome_campo)
        if val is not None:
            return val


def exibir_dataframe(registros: list[dict]) -> None:
    """Exibe qualquer lista de dicionários como DataFrame do Pandas."""
    if not registros:
        print('  Nenhum registro encontrado.')
        return
    df = pd.DataFrame(registros)
    print(df.to_string(index=False))


