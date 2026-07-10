CREATE TABLE Cliente (
    Cod_cliente SERIAL PRIMARY KEY,
    Nome        VARCHAR(120) NOT NULL,
    Cpf         CHAR(11) UNIQUE CHECK (Cpf ~ '^[0-9]{11}$'),
    Endereco    VARCHAR(200),
    Email       VARCHAR(120),
    Fone        VARCHAR(20)
);

CREATE TABLE Animal (
    Cod_animal      SERIAL PRIMARY KEY,
    Nome            VARCHAR(120) NOT NULL,
    Especie         VARCHAR(60),
    Data_nascimento DATE,
    Id_cliente      INTEGER NOT NULL REFERENCES Cliente (Cod_cliente) ON DELETE RESTRICT
);

CREATE TABLE Servico (
    Id_servico    SERIAL PRIMARY KEY,
    Tipo_servico  VARCHAR(80) NOT NULL,
    Valor         NUMERIC(10, 2) NOT NULL CHECK (Valor >= 0)
);

CREATE TABLE Funcionario (
    Id_funcionario SERIAL PRIMARY KEY,
    Nome           VARCHAR(120) NOT NULL,
    Cpf            CHAR(11) UNIQUE CHECK (Cpf ~ '^[0-9]{11}$'),
    Cargo          VARCHAR(60)
);

CREATE TABLE Veterinario (
    Id_funcionario INTEGER PRIMARY KEY REFERENCES Funcionario (Id_funcionario) ON DELETE CASCADE,
    Crmv           VARCHAR(30) NOT NULL
);

CREATE TABLE Tosador (
    Id_funcionario INTEGER PRIMARY KEY REFERENCES Funcionario (Id_funcionario) ON DELETE CASCADE,
    Especialidade  VARCHAR(80)
);

CREATE TABLE Agendamento (
    Id_agendamento SERIAL PRIMARY KEY,
    Data           DATE NOT NULL,
    Hora           TIME NOT NULL,
    Status         VARCHAR(20) NOT NULL DEFAULT 'Agendado',
    Cod_animal     INTEGER NOT NULL REFERENCES Animal (Cod_animal) ON DELETE RESTRICT,
    Id_funcionario INTEGER NOT NULL REFERENCES Funcionario (Id_funcionario) ON DELETE RESTRICT,
    Id_servico     INTEGER NOT NULL REFERENCES Servico (Id_servico) ON DELETE RESTRICT
);

CREATE TABLE Produto (
    Id_produto SERIAL PRIMARY KEY,
    Nome       VARCHAR(120) NOT NULL,
    Preco      NUMERIC(10, 2) NOT NULL CHECK (Preco >= 0),
    Estoque    INTEGER NOT NULL DEFAULT 0 CHECK (Estoque >= 0)
);

CREATE TABLE Venda (
    Id_venda       SERIAL PRIMARY KEY,
    Data           TIMESTAMP NOT NULL DEFAULT NOW(),
    Valor          NUMERIC(10, 2) NOT NULL DEFAULT 0,
    Id_cliente     INTEGER REFERENCES Cliente (Cod_cliente) ON DELETE SET NULL,
    Id_agendamento INTEGER REFERENCES Agendamento (Id_agendamento) ON DELETE SET NULL
);

CREATE TABLE Item_venda (
    Id_item_venda   SERIAL PRIMARY KEY,
    Id_venda        INTEGER NOT NULL REFERENCES Venda (Id_venda) ON DELETE CASCADE,
    Id_agendamento  INTEGER NOT NULL REFERENCES Agendamento (Id_agendamento) ON DELETE RESTRICT,
    Quantidade      INTEGER NOT NULL DEFAULT 1 CHECK (Quantidade > 0),
    Valor_unitario  NUMERIC(10, 2) NOT NULL CHECK (Valor_unitario >= 0),
    CONSTRAINT uq_itemvenda_agendamento UNIQUE (Id_agendamento)
);

CREATE TABLE Intem_Produto (
    Id_item_produto SERIAL PRIMARY KEY,
    Id_venda        INTEGER NOT NULL REFERENCES Venda (Id_venda) ON DELETE CASCADE,
    Id_produto      INTEGER NOT NULL REFERENCES Produto (Id_produto) ON DELETE RESTRICT,
    Quantidade      INTEGER NOT NULL DEFAULT 1 CHECK (Quantidade > 0),
    Valor_unitario  NUMERIC(10, 2) NOT NULL CHECK (Valor_unitario >= 0)
);

CREATE OR REPLACE FUNCTION fn_recalcula_valor_venda()
RETURNS TRIGGER AS $$
DECLARE
    v_id_venda INTEGER;
BEGIN
    v_id_venda := COALESCE(NEW.Id_venda, OLD.Id_venda);

    UPDATE Venda
    SET Valor = COALESCE((
        SELECT SUM(Quantidade * Valor_unitario) FROM Item_venda WHERE Id_venda = v_id_venda
    ), 0) + COALESCE((
        SELECT SUM(Quantidade * Valor_unitario) FROM Intem_Produto WHERE Id_venda = v_id_venda
    ), 0)
    WHERE Id_venda = v_id_venda;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_recalcula_valor_item_venda
AFTER INSERT OR UPDATE OR DELETE ON Item_venda
FOR EACH ROW EXECUTE FUNCTION fn_recalcula_valor_venda();

CREATE TRIGGER trg_recalcula_valor_item_produto
AFTER INSERT OR UPDATE OR DELETE ON Intem_Produto
FOR EACH ROW EXECUTE FUNCTION fn_recalcula_valor_venda();
