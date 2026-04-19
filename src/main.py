# Ponto de entrada da aplicação.
# Responsabilidade única: inicializar conexão, montar o menu e despachar rotinas.

import os
import sys

import config
import services.arquivos as arquivos
from db import database
from db.repositorio_insumo import InsumoRepositorio
from db.repositorio_movimentacao import MovimentacaoRepositorio
from cli.escritor import aguardar
from cli.rotinas_arquivo import rotina_exportar, rotina_importar, rotina_log
from cli.rotinas_insumo import (
    rotina_alterar,
    rotina_cadastrar,
    rotina_excluir,
    rotina_excluir_todos,
    rotina_listar,
)
from cli.rotinas_movimentacao import rotina_listar_movimentacoes, rotina_movimentacao
from cli.rotinas_relatorios import (
    rotina_relatorio_critico,
    rotina_relatorio_estoque,
    rotina_relatorio_movimentacoes,
)


def main() -> None:
    conn = None
    try:
        config.validar()
        conn = database.conectar()

        database.criar_tabelas(conn)
        arquivos.gravar_log('Sistema iniciado.')

        repo_insumo = InsumoRepositorio(conn)
        repo_mov    = MovimentacaoRepositorio(conn)

        _ACOES = {
            '1':  lambda: rotina_cadastrar(repo_insumo),
            '2':  lambda: rotina_listar(repo_insumo),
            '3':  lambda: rotina_movimentacao(repo_insumo, repo_mov),
            '4':  lambda: rotina_listar_movimentacoes(repo_insumo, repo_mov),
            '5':  lambda: rotina_alterar(repo_insumo),
            '6':  lambda: rotina_excluir(repo_insumo, repo_mov),
            '7':  lambda: rotina_excluir_todos(repo_insumo, repo_mov),
            '8':  lambda: rotina_relatorio_estoque(repo_insumo),
            '9':  lambda: rotina_relatorio_critico(repo_insumo),
            '10': lambda: rotina_relatorio_movimentacoes(repo_mov),
            '11': lambda: rotina_exportar(repo_insumo),
            '12': lambda: rotina_importar(repo_insumo),
            '13': rotina_log,
        }

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            print('\n' + '=' * 52)
            print('  CONTROLE DE INSUMOS AGRÍCOLAS')
            print('=' * 52)
            print("""
                1  Cadastrar insumo
                2  Listar insumos
                3  Registrar movimentação (entrada/saída)
                4  Listar movimentações
                5  Alterar insumo
                6  Excluir insumo
                7  EXCLUIR TODOS OS INSUMOS
                ──────────────────────────────────────
                8  Relatório: estoque atual (.csv)
                9  Relatório: estoque crítico (.csv)
                10 Relatório: movimentações (.csv)
                ──────────────────────────────────────
                11 Exportar insumos (.json)
                12 Importar insumos (.json)
                13 Exibir log do sistema
                ──────────────────────────────────────
                0  Sair
            """)
            escolha = input('  Escolha -> ').strip()

            if escolha == '0':
                arquivos.gravar_log('Sistema encerrado.')
                print('\n  Até logo!\n')
                break
            elif escolha in _ACOES:
                _ACOES[escolha]()
            else:
                print('  Opção inválida.')
    except EnvironmentError as e:
        print(f'\nERRO de configuração:\n  {e}\n')
        sys.exit(1)
    except database.ErroRepositorio as e:
        print(f'\n{e}\n')
        sys.exit(1)
    except Exception as e:
        print(f'\nERRO inesperado:\n  {e}\n')
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    main()
