CREATE TABLE `fato_transacoes _internacionais`(
    `id_fato` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sk_tempo` BIGINT NOT NULL,
    `sk_pais_origem` BIGINT NOT NULL,
    `sk_pais_destino` BIGINT NOT NULL,
    `sk_produto` BIGINT NOT NULL,
    `sk_moeda_origem` BIGINT NOT NULL,
    `sk_moeda_destino` BIGINT NOT NULL,
    `sk_tipo_transacao` BIGINT NOT NULL,
    `sk_transporte` BIGINT NOT NULL,
    `quantidade_transacionada` BIGINT NOT NULL,
    `valor_transacao` BIGINT NOT NULL,
    `valor_convertido` BIGINT NOT NULL,
    `taxa_cambio_aplicada` BIGINT NOT NULL
);
CREATE TABLE `dim_tempo`(
    `sk_tempo` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `data` DATE NOT NULL,
    `dia` INT NOT NULL,
    `mes` INT NOT NULL,
    `nome_mes` VARCHAR(20) NOT NULL,
    `trimestre` INT NOT NULL,
    `ano` INT NOT NULL,
    `dia_da_semana` VARCHAR(20) NOT NULL,
    `semestre` INT NOT NULL
);
CREATE TABLE `dim_pais`(
    `sk_pais` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `pais` VARCHAR(100) NOT NULL,
    `cod_iso` CHAR(3) NOT NULL,
    `bloco_economico` VARCHAR(100) NOT NULL
);
CREATE TABLE `dim_produto`(
    `sk_produto` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `produto` VARCHAR(150) NOT NULL,
    `ncm_produto` VARCHAR(20) NOT NULL,
    `categoria_produto` VARCHAR(100) NOT NULL
);
CREATE TABLE `dim_moeda`(
    `sk_moeda` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `descricao_moeda` VARCHAR(100) NOT NULL,
    `pais_moeda` VARCHAR(100) NOT NULL
);
CREATE TABLE `dim_tipo_transacao`(
    `sk_tipo_transacao` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `descricao_tipo_transacao` VARCHAR(100) NOT NULL
);
CREATE TABLE `dim_transporte`(
    `sk_transporte` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `descricao_transporte` BIGINT NOT NULL
);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_moeda_destino_foreign` FOREIGN KEY(`sk_moeda_destino`) REFERENCES `dim_moeda`(`sk_moeda`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_moeda_origem_foreign` FOREIGN KEY(`sk_moeda_origem`) REFERENCES `dim_moeda`(`sk_moeda`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_produto_foreign` FOREIGN KEY(`sk_produto`) REFERENCES `dim_produto`(`sk_produto`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_pais_origem_foreign` FOREIGN KEY(`sk_pais_origem`) REFERENCES `dim_pais`(`sk_pais`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_transporte_foreign` FOREIGN KEY(`sk_transporte`) REFERENCES `dim_transporte`(`sk_transporte`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_pais_destino_foreign` FOREIGN KEY(`sk_pais_destino`) REFERENCES `dim_pais`(`sk_pais`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_tipo_transacao_foreign` FOREIGN KEY(`sk_tipo_transacao`) REFERENCES `dim_tipo_transacao`(`sk_tipo_transacao`);
ALTER TABLE
    `fato_transacoes _internacionais` ADD CONSTRAINT `fato_transacoes _internacionais_sk_tempo_foreign` FOREIGN KEY(`sk_tempo`) REFERENCES `dim_tempo`(`sk_tempo`);