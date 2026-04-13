SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE fato_transacoes_internacionais;

TRUNCATE TABLE dim_tempo;
TRUNCATE TABLE dim_produto;
TRUNCATE TABLE dim_pais;
TRUNCATE TABLE dim_tipo_transacao;
TRUNCATE TABLE dim_transporte;
TRUNCATE TABLE dim_moeda;

SET FOREIGN_KEY_CHECKS = 1;