# Domínio de insumos: constantes, cálculos e validações puras.
# Sem I/O, sem print, sem acesso a banco — funções que apenas recebem e retornam valores.
#
# Categorias baseadas no material da atividade FIAP:
#   - SEMENTE, FERTILIZANTE, DEFENSIVO: citados explicitamente no Setor de Insumos
#   - CORRETIVO: calcário e gesso agrícola, prática padrão de manejo de solo
#   - COMBUSTIVEL: implícito pela menção a máquinas agrícolas e colheitadeiras
#   - OUTRO: catch-all para insumos não categorizados
#
# Referências: CROPLIFE Brasil (defensivos), EMBRAPA (variedades/sementes),
#              AGROTOOLS (gestão de insumos), atividade FIAP Fase 2.

CATEGORIAS = ('SEMENTE', 'FERTILIZANTE', 'DEFENSIVO', 'CORRETIVO', 'COMBUSTIVEL', 'OUTRO')
UNIDADES   = ('kg', 'L', 'un', 'sc', 't')   # kg, litros, unidades, sacas (60kg), toneladas


def calcular_valor_estoque(quantidade: float, preco_unit: float) -> float:
    """Retorna o valor total do estoque de um insumo (quantidade × preço unitário)."""
    return round(quantidade * preco_unit, 2)


def esta_em_estoque_critico(quantidade: float, estoque_min: float) -> bool:
    """Retorna True se a quantidade atual atingiu ou está abaixo do estoque mínimo."""
    return quantidade <= estoque_min


def validar_categoria(categoria: str) -> bool:
    """Retorna True se a categoria informada pertence à tupla CATEGORIAS."""
    return categoria.upper() in CATEGORIAS


def validar_unidade(unidade: str) -> bool:
    """Retorna True se a unidade informada pertence à tupla UNIDADES (case-insensitive)."""
    return unidade.lower() in {u.lower() for u in UNIDADES}


def validar_numero_positivo(texto: str, nome_campo: str) -> float | None:
    """
    Converte texto em float e verifica se o valor é positivo.
    Aceita vírgula como separador decimal.
    Retorna o valor convertido ou None em caso de erro — nunca lança exceção.
    """
    try:
        valor = float(texto.replace(',', '.'))
        if valor <= 0:
            print(f'  ERRO: {nome_campo} deve ser maior que zero.')
            return None
        return valor
    except ValueError:
        print(f'  ERRO: {nome_campo} deve ser um número.')
        return None


def validar_numero_nao_negativo(texto: str, nome_campo: str) -> float | None:
    """
    Igual a validar_numero_positivo, mas aceita zero.
    Usado para estoque inicial (pode ser cadastrado zerado).
    """
    try:
        valor = float(texto.replace(',', '.'))
        if valor < 0:
            print(f'  ERRO: {nome_campo} não pode ser negativo.')
            return None
        return valor
    except ValueError:
        print(f'  ERRO: {nome_campo} deve ser um número.')
        return None


