# Módulo de lógica de negócio para movimentações de estoque.
# Sem I/O e sem acesso a banco — apenas constantes e validações puras.

TIPOS_MOV = ('ENTRADA', 'SAIDA')   # entrada de estoque / saída para campo


def validar_tipo_mov(tipo: str) -> bool:
    """Retorna True se o tipo de movimentação pertence à tupla TIPOS_MOV."""
    return tipo.upper() in TIPOS_MOV
