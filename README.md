<div align="center">
<sub>Instituição: FIAP</sub>
</div>

# Controle de Insumos Agrícolas

## Nome do Grupo: Grupo 56

## 👨‍🎓 Integrantes
- Lucas Michels Kuntz - RM 570050
- João Pedro Alencar - RM 573473
- Camila Duarte Ferreira - RM 569629
- Thiago Henrique Piva Balerio - RM 572194
- Alisson Vinicius de Souza Rabelo Teixeira - RM 573512

## 👩‍🏫 Professores
### Tutor(a)
- <a href="#">Edson de Oliveira</a>
### Coordenador(a)
- <a href="#">André Godoi</a>

---

## 📜 Descrição

O **Setor de Insumos** é um dos cinco pilares do agronegócio: sem controle preciso de sementes, fertilizantes e defensivos, o produtor opera às cegas — comprando em excesso, desperdiçando por vencimento ou parando a safra por falta de produto no campo. Segundo a [AGROTOOLS](https://agrotools.com.br), falhas no controle de insumos podem representar perdas de até 20% do custo operacional da fazenda.

Este sistema permite ao produtor **cadastrar, movimentar e monitorar o estoque de insumos agrícolas** via terminal. Alertas automáticos de estoque crítico, rastreabilidade de entradas e saídas e relatórios CSV prontos para análise apoiam a tomada de decisão sobre reposição e planejamento de safra.

**Domínio escolhido:** Setor de Insumos — citado explicitamente na atividade como *"sementes, fertilizantes e defensivos agrícolas"*. Categorias fundamentadas em:
- [CROPLIFE Brasil](https://croplifebrasil.org) — defensivos agrícolas registrados
- [EMBRAPA](https://www.embrapa.br) — variedades de sementes e recomendações técnicas
- [AGROTOOLS](https://agrotools.com.br) — gestão de insumos e rastreabilidade

---

## 📁 Estrutura de Pastas

```
gs-python-agro/
│
├── assets/                              # Dados de seed
│   ├── insumos_amostra.json                 # 7 insumos de exemplo (estoque inicial)
│   └── movimentacoes_amostra.json           # 11 movimentações (3 itens ficam críticos)
│
├── config/                              # Configuração do ambiente
│   └── .env.example                         # Template de variáveis de ambiente
│
├── document/                            # Documentação do projeto
│   └── other/
│       ├── relatorio_estoque.csv            # gerado pela opção 8 do menu
│       ├── relatorio_critico.csv            # gerado pela opção 9 do menu
│       ├── relatorio_movimentacoes.csv      # gerado pela opção 10 do menu
│       └── insumos_export.json              # gerado pela opção 11 do menu
│
├── scripts/                             # Scripts auxiliares
│   ├── migration.sql                        # DDL das tabelas insumo e movimentacao (com FK)
│   └── seed.py                              # Popula o banco com dados de amostra
│
├── src/                                 # Código-fonte da aplicação
│   ├── main.py                              # Ponto de entrada: menu e despacho de rotinas
│   ├── config.py                            # Carregamento e validação do .env (fail-fast)
│   │
│   ├── db/                                  # Camada de banco de dados (Oracle)
│   │   ├── __init__.py
│   │   ├── database.py                      # Conexão Oracle e criação de tabelas
│   │   ├── repositorio_insumo.py            # CRUD da tabela insumo
│   │   └── repositorio_movimentacao.py      # CRUD da tabela movimentacao (transação atômica)
│   │
│   ├── services/                            # Lógica de negócio e utilitários
│   │   ├── __init__.py
│   │   ├── insumo.py                        # Domínio insumo: constantes, validações, cálculos
│   │   ├── movimentacao.py                  # Domínio movimentação: TIPOS_MOV e validação
│   │   ├── arquivos.py                      # Manipulação de arquivos: log .txt, JSON, CSV
│   │   └── relatorios.py                    # Montagem de tabelas de memória para CSV/exibição
│   │
│   └── cli/                                 # Interface de linha de comando
│       ├── __init__.py
│       ├── escritor.py                      # I/O de terminal: leitura com validação, exibição
│       ├── rotinas_insumo.py                # Controlador do CRUD de insumos
│       ├── rotinas_movimentacao.py          # Controlador de registro e listagem de movimentações
│       ├── rotinas_relatorios.py            # Controlador de geração de relatórios CSV
│       └── rotinas_arquivo.py               # Controlador de exportação/importação JSON e log
│
├── .env                                 # Credenciais locais (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Como Executar

### Pré-requisitos

- Python 3.10+
- Oracle SQL Developer com usuário FIAP configurado
- Acesso à rede `oracle.fiap.com.br`

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/LucasMichelsKuntz/gs-python-agro.git
cd gs-python-agro

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as credenciais do banco
cp config/.env.example .env
# Edite .env com seu RM e senha Oracle
```

### Execução

```bash
python src/main.py
```

> As tabelas `insumo` e `movimentacao` são criadas automaticamente na primeira execução.  
> Para criar manualmente, execute `scripts/migration.sql` no Oracle SQL Developer.

### Popular dados de amostra

```bash
python scripts/seed.py
```

O seed importa 7 insumos e aplica 11 movimentações realistas (plantio, adubação, calagem, abastecimento). Ao final, 3 itens ficam em estoque crítico:

| Insumo | Estoque Final | Mínimo | Status |
|---|---|---|---|
| Calcário Dolomítico PRNT 90 | 8 t | 15 t | **CRÍTICO** |
| Soja Intacta RR2 PRO | 5 sc | 20 sc | **CRÍTICO** |
| MAP Fosfato Monoamônico | 3 sc | 20 sc | **CRÍTICO** |

---

## 📋 Menu da Aplicação

```
1  Cadastrar insumo
2  Listar insumos
3  Registrar movimentação (entrada/saída)
4  Listar movimentações
5  Alterar insumo
6  Excluir insumo
7  EXCLUIR TODOS OS INSUMOS
────────────────────────────────────
8  Relatório: estoque atual (.csv)
9  Relatório: estoque crítico (.csv)
10 Relatório: movimentações (.csv)
────────────────────────────────────
11 Exportar insumos (.json)
12 Importar insumos (.json)
13 Exibir log do sistema
────────────────────────────────────
0  Sair
```

---

## 🗃 Conteúdo dos Capítulos Aplicado

### Cap. 3 — Subalgoritmos: funções e procedimentos com passagem de parâmetros

| Tipo | Exemplos | Arquivo |
|---|---|---|
| **Função** (retorna valor) | `calcular_valor_estoque(quantidade, preco_unit) -> float`, `esta_em_estoque_critico(...) -> bool`, `validar_categoria(categoria) -> bool`, `gerar_csv(dados, caminho) -> bool` | `services/insumo.py`, `services/arquivos.py` |
| **Procedimento** (sem retorno) | `exibir_cabecalho(titulo) -> None`, `gravar_log(mensagem) -> None`, `rotina_cadastrar(repo) -> None` | `cli/escritor.py`, `services/arquivos.py`, `cli/rotinas_insumo.py` |
| **Parâmetros tipados** | Todas as assinaturas usam type hints: `nome: str`, `quantidade: float`, `repo: InsumoRepositorio` | todos os módulos |
| **Importação de módulos** | `from services.insumo import CATEGORIAS, validar_categoria`, `from cli.escritor import ler_opcao, aguardar` | `cli/rotinas_insumo.py`, `cli/rotinas_movimentacao.py` |

### Cap. 4 — Estruturas de dados: lista, tupla, dicionário, tabela de memória

| Estrutura | Uso no projeto | Arquivo |
|---|---|---|
| **Tupla** (imutável) | `CATEGORIAS = ('SEMENTE','FERTILIZANTE',...)`, `UNIDADES = ('kg','L','un','sc','t')`, `TIPOS_MOV = ('ENTRADA','SAIDA')` — domínios fixos | `services/insumo.py`, `services/movimentacao.py` |
| **Dicionário** | Cada registro do banco retorna como `dict` com chaves `id`, `nome`, `quantidade`, etc. | `db/repositorio_insumo.py`, `db/repositorio_movimentacao.py` |
| **Lista** | `insumos: list[dict]` retornada pelo `listar()`, iterada para construir tabelas e relatórios | todos os repositórios |
| **Tabela de memória** (lista de dicionários) | `montar_estoque(insumos)` constrói `list[dict]` com colunas enriquecidas (Valor Total, Status) — exibida com Pandas e exportada como CSV | `services/relatorios.py` |

### Cap. 5 — Manipulação de arquivos: texto e JSON

| Recurso | Uso no projeto | Arquivo |
|---|---|---|
| **Arquivo texto — modo `'a'` (append)** | `gravar_log()` abre `sistema.log` em modo append com `open(caminho, 'a', encoding='utf-8')` — acrescenta linha sem apagar histórico | `services/arquivos.py` |
| **Gerenciador de contexto `with`** | Todo acesso a arquivo usa `with open(...) as arq:` — garante fechamento mesmo em erro | `services/arquivos.py` |
| **JSON — gravação** | `json.dump(dados, arq, ensure_ascii=False, indent=4)` exporta lista de insumos para `.json` | `services/arquivos.py` |
| **JSON — leitura** | `json.load(arq)` importa arquivo JSON e retorna lista de dicionários para cadastro em lote | `services/arquivos.py` |
| **CSV via Pandas** | `pd.DataFrame(dados).to_csv(caminho, index=False, encoding='utf-8-sig')` — BOM para compatibilidade Excel | `services/arquivos.py` |

### Cap. 6 — Tratamento de erros e conexão Oracle

| Recurso | Uso no projeto | Arquivo |
|---|---|---|
| **`try / except <Tipo> as e`** | `except ErroRepositorio as e` captura falhas do banco em todas as rotinas de interface | `cli/rotinas_*.py` |
| **Múltiplos `except`** | `except EnvironmentError`, `except database.ErroRepositorio`, `except Exception` — tratamento em camadas no ponto de entrada | `main.py` |
| **`else` no try** | Bloco `else:` executa apenas quando nenhuma exceção ocorre — usado em `rotina_cadastrar` e `rotina_movimentacao` para exibir mensagem de sucesso | `cli/rotinas_insumo.py`, `cli/rotinas_movimentacao.py` |
| **`finally`** | `conn.close()` no bloco `finally` garante que a conexão Oracle é encerrada independentemente de erro ou saída normal | `main.py` |
| **Exceção customizada** | `ErroRepositorio(Exception)` isola `oracledb` do restante da aplicação — a camada de apresentação só conhece este tipo | `db/database.py` |
| **Conexão Oracle** | `oracledb.connect(user, password, dsn)` com credenciais vindas do `.env` via `python-dotenv` | `db/database.py` |
| **CRUD Oracle** | `cursor.execute(sql, params)`, `cursor.fetchall()`, `conn.commit()`, `conn.rollback()` | `db/repositorio_insumo.py`, `db/repositorio_movimentacao.py` |
| **Transação atômica** | `SELECT ... FOR UPDATE` → valida estoque → `UPDATE insumo.quantidade` → `INSERT movimentacao` → `COMMIT` único; `rollback()` em caso de erro | `db/repositorio_movimentacao.py` |
| **Pandas — exibição** | `pd.DataFrame(registros).to_string(index=False)` para exibir tabelas de memória no terminal | `cli/escritor.py` |

---

## 🗄 Modelo de Dados

```sql
-- Tabela principal de insumos
CREATE TABLE insumo (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome          VARCHAR2(60)  NOT NULL,
    categoria     VARCHAR2(20)  NOT NULL CHECK (categoria IN ('SEMENTE','FERTILIZANTE','DEFENSIVO','CORRETIVO','COMBUSTIVEL','OUTRO')),
    unidade       VARCHAR2(5)   NOT NULL CHECK (unidade   IN ('kg','L','un','sc','t')),
    quantidade    NUMBER(12, 3) NOT NULL,
    estoque_min   NUMBER(12, 3) NOT NULL,
    preco_unit    NUMBER(10, 2) NOT NULL,
    fornecedor    VARCHAR2(60),
    data_cadastro DATE DEFAULT SYSDATE NOT NULL
);

-- Histórico de movimentações (FK para insumo)
CREATE TABLE movimentacao (
    id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    insumo_id  NUMBER        NOT NULL,
    tipo       VARCHAR2(10)  NOT NULL CHECK (tipo IN ('ENTRADA','SAIDA')),
    quantidade NUMBER(12, 3) NOT NULL,
    motivo     VARCHAR2(100),
    data_mov   DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT fk_mov_insumo FOREIGN KEY (insumo_id) REFERENCES insumo(id)
);
```

---

## 🗓 Histórico de Lançamentos

- **0.1.0** — 17/04/2026 — Estrutura inicial e CRUD Oracle
- **0.2.0** — 18/04/2026 — Exportação/importação JSON e log em arquivo texto
- **0.3.0** — 18/04/2026 — Reorganização conforme template FIAP
- **0.4.0** — 19/04/2026 — Domínio insumos agrícolas; duas entidades com FK; relatórios CSV; alertas de estoque crítico
- **0.5.0** — 19/04/2026 — Subpacotes `db/`, `services/`, `cli/`; domínios separados (`services/insumo.py` + `services/movimentacao.py`); saídas geradas em `document/other/`

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1">

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
  Este projeto está licenciado sob
  <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank">Attribution 4.0 International</a>.
</p>
