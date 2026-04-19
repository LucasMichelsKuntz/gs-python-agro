# Módulo de manipulação de arquivos: log em texto, dados em JSON e relatórios CSV.

import json
import os
from datetime import datetime

import pandas as pd

CAMINHO_LOG = 'sistema.log'


# ─── PROCEDIMENTOS (sem retorno) ───────────────────────────────────────────────

def gravar_log(mensagem: str) -> None:
    """
    Procedimento: acrescenta uma linha ao arquivo de log em modo append.
    Cria o arquivo automaticamente se não existir.
    """
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(CAMINHO_LOG, 'a', encoding='utf-8') as arq:
        arq.write(f'[{timestamp}] {mensagem}\n')


# ─── FUNÇÕES (retornam valor) ──────────────────────────────────────────────────

def exportar_json(registros: list, caminho: str) -> bool:
    """
    Serializa a lista de dicionários (tabela de memória) para arquivo JSON.
    Converte objetos datetime para string antes de gravar.
    Retorna True em caso de sucesso, False em caso de erro.
    """
    try:
        serializavel = []
        for r in registros:
            item = dict(r)
            if hasattr(item.get('data_registro'), 'strftime'):
                item['data_registro'] = item['data_registro'].strftime('%Y-%m-%d')
            serializavel.append(item)

        with open(caminho, 'w', encoding='utf-8') as arq:
            json.dump(serializavel, arq, ensure_ascii=False, indent=4)
        return True

    except Exception as e:
        print(f'  ERRO ao exportar JSON: {e}')
        return False


def importar_json(caminho: str) -> list | None:
    """
    Lê um arquivo JSON e retorna lista de dicionários (tabela de memória).
    Retorna None se o arquivo não existir ou estiver malformado.
    """
    try:
        with open(caminho, 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
        return dados

    except FileNotFoundError:
        print(f"  ERRO: Arquivo '{caminho}' não encontrado.")
        return None

    except json.JSONDecodeError:
        print('  ERRO: Arquivo JSON inválido ou corrompido.')
        return None


def exibir_log() -> None:
    """Procedimento: exibe o conteúdo do arquivo de log na tela."""
    if not os.path.exists(CAMINHO_LOG):
        print('  Nenhum log registrado ainda.')
        return

    print(f'\n  Conteúdo de {CAMINHO_LOG}:')
    print(f'  {"-" * 50}')
    with open(CAMINHO_LOG, 'r', encoding='utf-8') as arq:
        linhas = arq.readlines()

    ultimas = linhas[-20:] if len(linhas) > 20 else linhas
    for linha in ultimas:
        print(f'  {linha}', end='')

    if len(linhas) > 20:
        print(f'\n  ... ({len(linhas) - 20} linhas anteriores omitidas)')


def gerar_csv(dados: list[dict], caminho: str) -> bool:
    """
    Serializa lista de dicionários (tabela de memória) para arquivo CSV.
    Usa encoding utf-8-sig (BOM) para compatibilidade com Excel no Windows.
    Retorna True em caso de sucesso, False em caso de erro.
    """
    try:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        pd.DataFrame(dados).to_csv(caminho, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        print(f'  ERRO ao gerar CSV: {e}')
        return False
