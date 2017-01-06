-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: TicketDb
-- ------------------------------------------------------
-- Server version	5.7.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Activity`
--

DROP TABLE IF EXISTS `Activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Activity` (
  `ID` decimal(5,2) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Date` date NOT NULL,
  `TicketsLeft` decimal(5,2) NOT NULL,
  `Type` varchar(20) NOT NULL,
  `ShowroomID` decimal(5,2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Type` (`Type`),
  KEY `ShowroomID` (`ShowroomID`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`Type`) REFERENCES `Types` (`Type`),
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`ShowroomID`) REFERENCES `ShowroomMain` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Activity`
--

LOCK TABLES `Activity` WRITE;
/*!40000 ALTER TABLE `Activity` DISABLE KEYS */;
INSERT INTO `Activity` VALUES (2.00,'Tiratro','2017-01-02',1.00,'Theatre',5.00),(3.00,'Uzayli Onurcan','2017-01-04',25.00,'Cinema',3.00),(4.00,'Anilla Dans Keyfi','2017-02-01',5.00,'Dance',2.00),(5.00,'Ben Avustralyadayken','2017-03-01',4.00,'Cinema',4.00),(6.00,'Onurcanin Ic Dunyasi','2017-05-01',3.00,'Opera',5.00),(7.00,'Bir coderin drami','2017-03-01',13.00,'Cinema',3.00),(8.00,'Balet Anil Show','2017-09-01',5.00,'Opera',2.00),(9.00,'Onurcanla Oryantel','2017-10-01',5.00,'Dance',2.00),(10.00,'Datashock Documentry','2017-11-01',4.00,'Cinema',4.00),(11.00,'Baturayla devri alem','2017-06-01',3.00,'Theatre',4.00),(12.00,'Onurcan Ivedik','2017-01-11',3.00,'Cinema',5.00),(13.00,'Big Bang Theory','2017-01-21',37.00,'Cinema',3.00);
/*!40000 ALTER TABLE `Activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cities`
--

DROP TABLE IF EXISTS `Cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cities` (
  `City` varchar(20) NOT NULL,
  PRIMARY KEY (`City`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cities`
--

LOCK TABLES `Cities` WRITE;
/*!40000 ALTER TABLE `Cities` DISABLE KEYS */;
INSERT INTO `Cities` VALUES ('Bursa'),('Istanbul'),('Izmir'),('Trabzon');
/*!40000 ALTER TABLE `Cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reservations`
--

DROP TABLE IF EXISTS `Reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Reservations` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NumberOfPeople` decimal(2,0) NOT NULL,
  `Email` varchar(20) NOT NULL,
  `ActivityID` decimal(5,2) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Email` (`Email`),
  KEY `ActivityID` (`ActivityID`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `User` (`Email`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`ActivityID`) REFERENCES `Activity` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reservations`
--

LOCK TABLES `Reservations` WRITE;
/*!40000 ALTER TABLE `Reservations` DISABLE KEYS */;
INSERT INTO `Reservations` VALUES (61,1,'baturay@live.fr',11.00),(62,2,'baturay@live.fr',13.00);
/*!40000 ALTER TABLE `Reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ShowroomCapacity`
--

DROP TABLE IF EXISTS `ShowroomCapacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ShowroomCapacity` (
  `Name` varchar(20) NOT NULL,
  `Capacity` decimal(5,2) NOT NULL,
  `City` varchar(20) NOT NULL,
  PRIMARY KEY (`Name`,`City`),
  KEY `City` (`City`),
  CONSTRAINT `showroomcapacity_ibfk_1` FOREIGN KEY (`City`) REFERENCES `Cities` (`City`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ShowroomCapacity`
--

LOCK TABLES `ShowroomCapacity` WRITE;
/*!40000 ALTER TABLE `ShowroomCapacity` DISABLE KEYS */;
INSERT INTO `ShowroomCapacity` VALUES ('Forum Trabzon',3.00,'Trabzon'),('Izmir Alsancak',2.00,'Izmir'),('Jolly Joker Bursa',5.00,'Bursa'),('Kucuk Ciftlik Park',4.00,'Istanbul');
/*!40000 ALTER TABLE `ShowroomCapacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ShowroomMain`
--

DROP TABLE IF EXISTS `ShowroomMain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ShowroomMain` (
  `ID` decimal(5,2) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `City` varchar(20) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `City` (`City`),
  CONSTRAINT `showroommain_ibfk_1` FOREIGN KEY (`City`) REFERENCES `Cities` (`City`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ShowroomMain`
--

LOCK TABLES `ShowroomMain` WRITE;
/*!40000 ALTER TABLE `ShowroomMain` DISABLE KEYS */;
INSERT INTO `ShowroomMain` VALUES (2.00,'Jolly Joker Bursa','Bursa'),(3.00,'Izmir Alsancak','Izmir'),(4.00,'Kucuk Ciftlik Park','Istanbul'),(5.00,'Forum Trabzon','Trabzon');
/*!40000 ALTER TABLE `ShowroomMain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Types`
--

DROP TABLE IF EXISTS `Types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Types` (
  `Type` varchar(20) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Types`
--

LOCK TABLES `Types` WRITE;
/*!40000 ALTER TABLE `Types` DISABLE KEYS */;
INSERT INTO `Types` VALUES ('Cinema'),('Dance'),('Opera'),('Theatre');
/*!40000 ALTER TABLE `Types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `Email` varchar(50) NOT NULL,
  `Password` varchar(60) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Surname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES ('baturay@live.fr','3232','baturay','ofluoglu');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-01-02 23:20:33
