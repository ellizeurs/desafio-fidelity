-- ================================
-- Tabela: estado
-- ================================
CREATE TABLE estado (
  Cod_UF INT PRIMARY KEY,
  Cod_Fornecedor INT,
  UF CHAR(2),
  Nome TEXT
);

-- ================================
-- Tabela: servico
-- ================================
CREATE TABLE servico (
  cod_servico INT PRIMARY KEY,
  civel BOOLEAN,
  criminal BOOLEAN
);

-- ================================
-- Tabela: pesquisa
-- ================================
CREATE TABLE pesquisa (
  cod_pesquisa INT PRIMARY KEY,
  cod_cliente INT FOREIGN,
  cod_servico INT REFERENCES servico(cod_servico),
  cod_uf INT REFERENCES estado(Cod_UF),
  tipo INT,
  cpf VARCHAR(14),
  cod_uf_nascimento INT REFERENCES estado(Cod_UF),
  cod_uf_rg INT REFERENCES estado(Cod_UF),
  data_entrada TIMESTAMP,
  data_conclusao TIMESTAMP,
  nome TEXT,
  nome_corrigido TEXT,
  rg VARCHAR(20),
  rg_corrigido VARCHAR(20),
  nascimento DATE,
  mae TEXT,
  mae_corrigido TEXT,
  anexo TEXT
);

-- ================================
-- Tabela: lote
-- ================================
CREATE TABLE lote (
  Cod_Lote INT PRIMARY KEY,
  Cod_Lote_Prazo DATE,
  Data_Criacao TIMESTAMP,
  Cod_Funcionario INT,
  Tipo TEXT,
  Prioridade TEXT
);

-- ================================
-- Tabela: lote_pesquisa
-- ================================
CREATE TABLE lote_pesquisa (
  Cod_Lote_Pesquisa INT PRIMARY KEY,
  Cod_Lote INT REFERENCES lote(Cod_Lote),
  Cod_Pesquisa INT REFERENCES pesquisa(cod_pesquisa),
  Cod_Funcionario INT,
  Cod_Funcionario_Conclusao INT,
  Cod_Fornecedor INT,
  Data_Entrada TIMESTAMP,
  Data_Conclusao TIMESTAMP,
  Cod_UF INT REFERENCES estado(Cod_UF),
  Obs TEXT
);

-- ================================
-- Tabela: pesquisa_spv
-- ================================
CREATE TABLE pesquisa_spv (
  cod_pesquisa INT REFERENCES pesquisa(cod_pesquisa),
  cod_spv INT,
  cod_spv_computador INT,
  cod_spv_tipo INT,
  cod_funcionario INT,
  filtro INT,
  website_id INT,
  resultado INT,
  PRIMARY KEY (cod_pesquisa, cod_spv)
);
