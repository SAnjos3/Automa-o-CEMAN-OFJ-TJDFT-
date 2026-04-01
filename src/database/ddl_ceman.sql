-- =============================================================================
-- DDL - CEMAN Automação - Oracle APEX
-- Autor: Equipe CEMAN
-- Descrição: Scripts de criação das tabelas e sequências do sistema.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tabela: MANDADOS
-- Armazena os mandados extraídos do portal CEMAN.
-- -----------------------------------------------------------------------------
CREATE TABLE MANDADOS (
    ID               NUMBER        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    PROCESSO         VARCHAR2(50)  NOT NULL,
    TIPO_ATO         VARCHAR2(100) NOT NULL,
    NOME_PARTES      VARCHAR2(500),
    ENDERECO         VARCHAR2(500),
    VARA             VARCHAR2(200),
    PRAZO            DATE,
    STATUS           VARCHAR2(50)  DEFAULT 'Pendente' NOT NULL,
    PDF_PATH         VARCHAR2(500),
    OFICIAL_ID       NUMBER,
    CRIADO_EM        TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL,
    ATUALIZADO_EM    TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL,
    CONSTRAINT CHK_STATUS_MANDADO CHECK (
        STATUS IN ('Pendente', 'Em Cumprimento', 'Cumprido', 'Não Localizado', 'Devolvido')
    )
);

COMMENT ON TABLE  MANDADOS             IS 'Mandados judiciais extraídos do portal CEMAN.';
COMMENT ON COLUMN MANDADOS.PROCESSO    IS 'Número único do processo judicial (ex.: 0000000-00.0000.8.07.0000).';
COMMENT ON COLUMN MANDADOS.TIPO_ATO    IS 'Tipo do ato judicial (Citação, Intimação, Penhora, etc.).';
COMMENT ON COLUMN MANDADOS.STATUS      IS 'Status atual do cumprimento do mandado.';
COMMENT ON COLUMN MANDADOS.OFICIAL_ID  IS 'Referência ao Oficial de Justiça responsável.';


-- -----------------------------------------------------------------------------
-- Tabela: OFICIAIS
-- Cadastro dos Oficiais de Justiça.
-- -----------------------------------------------------------------------------
CREATE TABLE OFICIAIS (
    ID             NUMBER        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NOME           VARCHAR2(200) NOT NULL,
    MATRICULA      VARCHAR2(20)  NOT NULL UNIQUE,
    WHATSAPP       VARCHAR2(20),
    EMAIL          VARCHAR2(150),
    ATIVO          NUMBER(1)     DEFAULT 1 NOT NULL,
    CRIADO_EM      TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL
);

COMMENT ON TABLE  OFICIAIS           IS 'Cadastro de Oficiais de Justiça do TJDFT.';
COMMENT ON COLUMN OFICIAIS.MATRICULA IS 'Matrícula funcional do servidor.';
COMMENT ON COLUMN OFICIAIS.WHATSAPP  IS 'Número WhatsApp no formato internacional (ex.: 5561999999999).';


-- -----------------------------------------------------------------------------
-- Tabela: HISTORICO_MANDADOS
-- Registra todas as mudanças de status dos mandados.
-- -----------------------------------------------------------------------------
CREATE TABLE HISTORICO_MANDADOS (
    ID            NUMBER        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MANDADO_ID    NUMBER        NOT NULL REFERENCES MANDADOS(ID) ON DELETE CASCADE,
    STATUS_ANTERIOR VARCHAR2(50),
    STATUS_NOVO   VARCHAR2(50)  NOT NULL,
    OBSERVACAO    VARCHAR2(1000),
    OFICIAL_ID    NUMBER        REFERENCES OFICIAIS(ID),
    CRIADO_EM     TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL
);

COMMENT ON TABLE  HISTORICO_MANDADOS IS 'Histórico de alterações de status dos mandados.';


-- -----------------------------------------------------------------------------
-- Tabela: CERTIDOES
-- Certidões geradas automaticamente após o cumprimento dos mandados.
-- -----------------------------------------------------------------------------
CREATE TABLE CERTIDOES (
    ID            NUMBER        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MANDADO_ID    NUMBER        NOT NULL REFERENCES MANDADOS(ID) ON DELETE CASCADE,
    CONTEUDO      CLOB,
    PDF_PATH      VARCHAR2(500),
    GERADO_EM     TIMESTAMP     DEFAULT SYSTIMESTAMP NOT NULL,
    ASSINADO      NUMBER(1)     DEFAULT 0 NOT NULL
);

COMMENT ON TABLE  CERTIDOES          IS 'Certidões de cumprimento de mandado geradas pelo sistema.';
COMMENT ON COLUMN CERTIDOES.ASSINADO IS '1 = Assinado digitalmente; 0 = Aguardando assinatura.';


-- -----------------------------------------------------------------------------
-- Foreign key: MANDADOS -> OFICIAIS
-- -----------------------------------------------------------------------------
ALTER TABLE MANDADOS
    ADD CONSTRAINT FK_MANDADO_OFICIAL
    FOREIGN KEY (OFICIAL_ID) REFERENCES OFICIAIS(ID);


-- -----------------------------------------------------------------------------
-- Índices
-- -----------------------------------------------------------------------------
CREATE INDEX IDX_MANDADOS_STATUS    ON MANDADOS (STATUS);
CREATE INDEX IDX_MANDADOS_OFICIAL   ON MANDADOS (OFICIAL_ID);
CREATE INDEX IDX_HIST_MANDADO_ID    ON HISTORICO_MANDADOS (MANDADO_ID);


-- -----------------------------------------------------------------------------
-- Trigger: Atualiza ATUALIZADO_EM ao modificar um mandado
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_MANDADOS_UPD
    BEFORE UPDATE ON MANDADOS
    FOR EACH ROW
BEGIN
    :NEW.ATUALIZADO_EM := SYSTIMESTAMP;
END;
/
