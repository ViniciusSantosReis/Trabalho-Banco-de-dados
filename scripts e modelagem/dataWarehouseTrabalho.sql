-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dw_comex
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dim_moeda`
--

DROP TABLE IF EXISTS `dim_moeda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_moeda` (
  `sk_moeda` bigint NOT NULL,
  `descricao_moeda` varchar(100) DEFAULT NULL,
  `pais_moeda` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sk_moeda`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_pais`
--

DROP TABLE IF EXISTS `dim_pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_pais` (
  `sk_pais` bigint NOT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `cod_iso` char(3) DEFAULT NULL,
  `bloco_economico` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sk_pais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_produto`
--

DROP TABLE IF EXISTS `dim_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_produto` (
  `sk_produto` bigint NOT NULL,
  `produto` varchar(255) DEFAULT NULL,
  `ncm_produto` varchar(20) DEFAULT NULL,
  `categoria_produto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sk_produto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_tempo`
--

DROP TABLE IF EXISTS `dim_tempo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_tempo` (
  `sk_tempo` bigint NOT NULL,
  `data` date DEFAULT NULL,
  `dia` int DEFAULT NULL,
  `mes` int DEFAULT NULL,
  `nome_mes` varchar(20) DEFAULT NULL,
  `trimestre` int DEFAULT NULL,
  `ano` int DEFAULT NULL,
  `dia_da_semana` varchar(20) DEFAULT NULL,
  `semestre` int DEFAULT NULL,
  PRIMARY KEY (`sk_tempo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_tipo_transacao`
--

DROP TABLE IF EXISTS `dim_tipo_transacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_tipo_transacao` (
  `sk_tipo_transacao` bigint NOT NULL,
  `descricao_tipo_transacao` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sk_tipo_transacao`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dim_transporte`
--

DROP TABLE IF EXISTS `dim_transporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dim_transporte` (
  `sk_transporte` bigint NOT NULL,
  `descricao_transporte` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sk_transporte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fato_transacoes_internacionais`
--

DROP TABLE IF EXISTS `fato_transacoes_internacionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fato_transacoes_internacionais` (
  `id_fato` bigint NOT NULL AUTO_INCREMENT,
  `sk_tempo` bigint DEFAULT NULL,
  `sk_pais_origem` bigint DEFAULT NULL,
  `sk_pais_destino` bigint DEFAULT NULL,
  `sk_produto` bigint DEFAULT NULL,
  `sk_moeda_origem` bigint DEFAULT NULL,
  `sk_moeda_destino` bigint DEFAULT NULL,
  `sk_tipo_transacao` bigint DEFAULT NULL,
  `sk_transporte` bigint DEFAULT NULL,
  `quantidade_transacionada` bigint DEFAULT NULL,
  `valor_transacao` decimal(18,2) DEFAULT NULL,
  `valor_convertido` decimal(18,2) DEFAULT NULL,
  `taxa_cambio_aplicada` decimal(18,6) DEFAULT NULL,
  PRIMARY KEY (`id_fato`),
  KEY `sk_tempo` (`sk_tempo`),
  KEY `sk_pais_origem` (`sk_pais_origem`),
  KEY `sk_pais_destino` (`sk_pais_destino`),
  KEY `sk_produto` (`sk_produto`),
  KEY `sk_moeda_origem` (`sk_moeda_origem`),
  KEY `sk_moeda_destino` (`sk_moeda_destino`),
  KEY `sk_tipo_transacao` (`sk_tipo_transacao`),
  KEY `sk_transporte` (`sk_transporte`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_1` FOREIGN KEY (`sk_tempo`) REFERENCES `dim_tempo` (`sk_tempo`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_2` FOREIGN KEY (`sk_pais_origem`) REFERENCES `dim_pais` (`sk_pais`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_3` FOREIGN KEY (`sk_pais_destino`) REFERENCES `dim_pais` (`sk_pais`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_4` FOREIGN KEY (`sk_produto`) REFERENCES `dim_produto` (`sk_produto`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_5` FOREIGN KEY (`sk_moeda_origem`) REFERENCES `dim_moeda` (`sk_moeda`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_6` FOREIGN KEY (`sk_moeda_destino`) REFERENCES `dim_moeda` (`sk_moeda`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_7` FOREIGN KEY (`sk_tipo_transacao`) REFERENCES `dim_tipo_transacao` (`sk_tipo_transacao`),
  CONSTRAINT `fato_transacoes_internacionais_ibfk_8` FOREIGN KEY (`sk_transporte`) REFERENCES `dim_transporte` (`sk_transporte`)
) ENGINE=InnoDB AUTO_INCREMENT=12496 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 11:21:47
