-- DDL do sistema de Controle de Insumos Agrícolas.
-- Execute no Oracle SQL Developer antes de rodar a aplicação,
-- ou deixe a aplicação criar as tabelas automaticamente na primeira execução (src/database.py).

CREATE TABLE insumo (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome          VARCHAR2(60)  NOT NULL,
    categoria     VARCHAR2(20)  NOT NULL,
    unidade       VARCHAR2(5)   NOT NULL,
    quantidade    NUMBER(12, 3) NOT NULL,   -- estoque atual (atualizado via movimentacao)
    estoque_min   NUMBER(12, 3) NOT NULL,   -- limiar de alerta de estoque crítico
    preco_unit    NUMBER(10, 2) NOT NULL,
    fornecedor    VARCHAR2(60),
    data_cadastro DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT chk_insumo_categoria CHECK (
        categoria IN ('SEMENTE','FERTILIZANTE','DEFENSIVO','CORRETIVO','COMBUSTIVEL','OUTRO')
    ),
    CONSTRAINT chk_insumo_unidade CHECK (
        unidade IN ('kg','L','un','sc','t')
    )
);

CREATE TABLE movimentacao (
    id         NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    insumo_id  NUMBER        NOT NULL,
    tipo       VARCHAR2(10)  NOT NULL,
    quantidade NUMBER(12, 3) NOT NULL,
    motivo     VARCHAR2(100),
    data_mov   DATE DEFAULT SYSDATE NOT NULL,
    CONSTRAINT chk_mov_tipo     CHECK (tipo IN ('ENTRADA','SAIDA')),
    CONSTRAINT fk_mov_insumo    FOREIGN KEY (insumo_id) REFERENCES insumo(id)
);
