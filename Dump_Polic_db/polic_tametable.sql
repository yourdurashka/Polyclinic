-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: polic
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `tametable`
--

DROP TABLE IF EXISTS `tametable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tametable` (
  `id_timetab` int NOT NULL AUTO_INCREMENT,
  `date_visit` varchar(100) NOT NULL,
  `visit` varchar(45) DEFAULT NULL,
  `id_doc` int DEFAULT NULL,
  `id_cab` int DEFAULT NULL,
  `id_card` int DEFAULT NULL,
  PRIMARY KEY (`id_timetab`),
  KEY `cabinet_idk_idx` (`id_cab`),
  KEY `doctor_idk_idx` (`id_doc`),
  KEY `pacients_idk_idx` (`id_card`),
  CONSTRAINT `cabinet_idk` FOREIGN KEY (`id_cab`) REFERENCES `cabinet` (`id_cab`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `doctor_idk` FOREIGN KEY (`id_doc`) REFERENCES `doctor` (`id_doc`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `pacients_idk` FOREIGN KEY (`id_card`) REFERENCES `paclent` (`id_pac`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tametable`
--

LOCK TABLES `tametable` WRITE;
/*!40000 ALTER TABLE `tametable` DISABLE KEYS */;
INSERT INTO `tametable` VALUES (1,'2022-12-25','+',111,1,1),(2,'2022-12-27','+',222,2,2),(3,'2022-12-31','+',333,3,3),(4,'2022-12-30',NULL,111,1,1);
/*!40000 ALTER TABLE `tametable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-04 19:01:23
