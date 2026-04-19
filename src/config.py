import os
from pathlib import Path
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / '.env')

DB_USUARIO = os.getenv('DB_USUARIO', '')
DB_SENHA   = os.getenv('DB_SENHA', '')
DB_DSN     = os.getenv('DB_DSN', '')

_OBRIGATORIAS = {'DB_USUARIO': DB_USUARIO, 'DB_SENHA': DB_SENHA, 'DB_DSN': DB_DSN}

"""Interrompe a aplicação imediatamente se alguma variável obrigatória estiver ausente."""
def validar() -> None:
    ausentes = [k for k, v in _OBRIGATORIAS.items() if not v]
    if ausentes:
        raise EnvironmentError(
            f"Variáveis ausentes no .env: {', '.join(ausentes)}\n"
            "Copie config/.env.example para .env na raiz e preencha as credenciais."
        )
