-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: antdvue
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add captcha store',7,'add_captchastore'),(26,'Can change captcha store',7,'change_captchastore'),(27,'Can delete captcha store',7,'delete_captchastore'),(28,'Can view captcha store',7,'view_captchastore'),(29,'Can add 职级表',8,'add_level'),(30,'Can change 职级表',8,'change_level'),(31,'Can delete 职级表',8,'delete_level'),(32,'Can view 职级表',8,'view_level'),(33,'Can add 岗位表',9,'add_position'),(34,'Can change 岗位表',9,'change_position'),(35,'Can delete 岗位表',9,'delete_position'),(36,'Can view 岗位表',9,'view_position'),(37,'Can add 部门表',10,'add_dept'),(38,'Can change 部门表',10,'change_dept'),(39,'Can delete 部门表',10,'delete_dept'),(40,'Can view 部门表',10,'view_dept'),(41,'Can add 角色表',11,'add_role'),(42,'Can change 角色表',11,'change_role'),(43,'Can delete 角色表',11,'delete_role'),(44,'Can view 角色表',11,'view_role'),(45,'Can add 角色菜单表',12,'add_rolemenu'),(46,'Can change 角色菜单表',12,'change_rolemenu'),(47,'Can delete 角色菜单表',12,'delete_rolemenu'),(48,'Can view 角色菜单表',12,'view_rolemenu'),(49,'Can add 城市表',13,'add_city'),(50,'Can change 城市表',13,'change_city'),(51,'Can delete 城市表',13,'delete_city'),(52,'Can view 城市表',13,'view_city'),(53,'Can add 站点表',14,'add_item'),(54,'Can change 站点表',14,'change_item'),(55,'Can delete 站点表',14,'delete_item'),(56,'Can view 站点表',14,'view_item'),(57,'Can add 栏目表',15,'add_itemcate'),(58,'Can change 栏目表',15,'change_itemcate'),(59,'Can delete 栏目表',15,'delete_itemcate'),(60,'Can view 栏目表',15,'view_itemcate'),(61,'Can add 友链表',16,'add_link'),(62,'Can change 友链表',16,'change_link'),(63,'Can delete 友链表',16,'delete_link'),(64,'Can view 友链表',16,'view_link'),(65,'Can add 广告位表',17,'add_adsort'),(66,'Can change 广告位表',17,'change_adsort'),(67,'Can delete 广告位表',17,'delete_adsort'),(68,'Can view 广告位表',17,'view_adsort'),(69,'Can add 广告表',18,'add_ad'),(70,'Can change 广告表',18,'change_ad'),(71,'Can delete 广告表',18,'delete_ad'),(72,'Can view 广告表',18,'view_ad'),(73,'Can add 通知公告表',19,'add_notice'),(74,'Can change 通知公告表',19,'change_notice'),(75,'Can delete 通知公告表',19,'delete_notice'),(76,'Can view 通知公告表',19,'view_notice'),(77,'Can add 用户表',20,'add_user'),(78,'Can change 用户表',20,'change_user'),(79,'Can delete 用户表',20,'delete_user'),(80,'Can view 用户表',20,'view_user'),(81,'Can add 用户角色表',21,'add_userrole'),(82,'Can change 用户角色表',21,'change_userrole'),(83,'Can delete 用户角色表',21,'delete_userrole'),(84,'Can view 用户角色表',21,'view_userrole'),(85,'Can add 会员等级表',22,'add_memberlevel'),(86,'Can change 会员等级表',22,'change_memberlevel'),(87,'Can delete 会员等级表',22,'delete_memberlevel'),(88,'Can view 会员等级表',22,'view_memberlevel'),(89,'Can add 会员表',23,'add_member'),(90,'Can change 会员表',23,'change_member'),(91,'Can delete 会员表',23,'delete_member'),(92,'Can view 会员表',23,'view_member'),(93,'Can add 字典表',24,'add_dict'),(94,'Can change 字典表',24,'change_dict'),(95,'Can delete 字典表',24,'delete_dict'),(96,'Can view 字典表',24,'view_dict'),(97,'Can add 字典项表',25,'add_dictdata'),(98,'Can change 字典项表',25,'change_dictdata'),(99,'Can delete 字典项表',25,'delete_dictdata'),(100,'Can view 字典项表',25,'view_dictdata'),(101,'Can add 配置表',26,'add_config'),(102,'Can change 配置表',26,'change_config'),(103,'Can delete 配置表',26,'delete_config'),(104,'Can view 配置表',26,'view_config'),(105,'Can add 配置项表',27,'add_configdata'),(106,'Can change 配置项表',27,'change_configdata'),(107,'Can delete 配置项表',27,'delete_configdata'),(108,'Can view 配置项表',27,'view_configdata'),(109,'Can add 菜单表',28,'add_menu'),(110,'Can change 菜单表',28,'change_menu'),(111,'Can delete 菜单表',28,'delete_menu'),(112,'Can view 菜单表',28,'view_menu'),(113,'Can add eyeglass frame material type',29,'add_eyeglassframematerialtype'),(114,'Can change eyeglass frame material type',29,'change_eyeglassframematerialtype'),(115,'Can delete eyeglass frame material type',29,'delete_eyeglassframematerialtype'),(116,'Can view eyeglass frame material type',29,'view_eyeglassframematerialtype'),(117,'Can add eyeglass frame color type',30,'add_eyeglassframecolortype'),(118,'Can change eyeglass frame color type',30,'change_eyeglassframecolortype'),(119,'Can delete eyeglass frame color type',30,'delete_eyeglassframecolortype'),(120,'Can view eyeglass frame color type',30,'view_eyeglassframecolortype'),(121,'Can add eyeglass frame shape type',31,'add_eyeglassframeshapetype'),(122,'Can change eyeglass frame shape type',31,'change_eyeglassframeshapetype'),(123,'Can delete eyeglass frame shape type',31,'delete_eyeglassframeshapetype'),(124,'Can view eyeglass frame shape type',31,'view_eyeglassframeshapetype'),(125,'Can add eyeglass frame entry',32,'add_eyeglassframeentry'),(126,'Can change eyeglass frame entry',32,'change_eyeglassframeentry'),(127,'Can delete eyeglass frame entry',32,'delete_eyeglassframeentry'),(128,'Can view eyeglass frame entry',32,'view_eyeglassframeentry'),(129,'Can add eyeglass frame style type',33,'add_eyeglassframestyletype'),(130,'Can change eyeglass frame style type',33,'change_eyeglassframestyletype'),(131,'Can delete eyeglass frame style type',33,'delete_eyeglassframestyletype'),(132,'Can view eyeglass frame style type',33,'view_eyeglassframestyletype'),(133,'Can add eyeglass frame entry style',34,'add_eyeglassframeentrystyle'),(134,'Can change eyeglass frame entry style',34,'change_eyeglassframeentrystyle'),(135,'Can delete eyeglass frame entry style',34,'delete_eyeglassframeentrystyle'),(136,'Can view eyeglass frame entry style',34,'view_eyeglassframeentrystyle'),(137,'Can add eyeglass frame detection result',35,'add_eyeglassframedetectionresult'),(138,'Can change eyeglass frame detection result',35,'change_eyeglassframedetectionresult'),(139,'Can delete eyeglass frame detection result',35,'delete_eyeglassframedetectionresult'),(140,'Can view eyeglass frame detection result',35,'view_eyeglassframedetectionresult'),(141,'Can add eyeglass frame recommandation request',36,'add_eyeglassframerecommandationrequest'),(142,'Can change eyeglass frame recommandation request',36,'change_eyeglassframerecommandationrequest'),(143,'Can delete eyeglass frame recommandation request',36,'delete_eyeglassframerecommandationrequest'),(144,'Can view eyeglass frame recommandation request',36,'view_eyeglassframerecommandationrequest');
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `captcha_captchastore` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_ad`
--

DROP TABLE IF EXISTS `django_ad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_ad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(255) NOT NULL,
  `sort_id` int NOT NULL,
  `type` int NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `width` int NOT NULL,
  `height` int NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `end_time` datetime(6) DEFAULT NULL,
  `click` int NOT NULL,
  `status` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  `content` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_ad`
--

LOCK TABLES `django_ad` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_ad_sort`
--

DROP TABLE IF EXISTS `django_ad_sort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_ad_sort` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `item_id` int NOT NULL,
  `cate_id` int NOT NULL,
  `loc_id` int NOT NULL,
  `platform` int NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_ad_sort`
--

LOCK TABLES `django_ad_sort` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_city`
--

DROP TABLE IF EXISTS `django_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_city` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `city_code` varchar(6) NOT NULL,
  `area_code` varchar(20) NOT NULL,
  `parent_code` varchar(20) DEFAULT NULL,
  `zip_code` varchar(6) NOT NULL,
  `level` int NOT NULL,
  `pid` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `short_name` varchar(150) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `pinyin` varchar(150) DEFAULT NULL,
  `lng` varchar(150) DEFAULT NULL,
  `lat` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_city`
--

LOCK TABLES `django_city` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_config`
--

DROP TABLE IF EXISTS `django_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_config`
--

LOCK TABLES `django_config` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_config_data`
--

DROP TABLE IF EXISTS `django_config_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_config_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(150) NOT NULL,
  `code` varchar(150) NOT NULL,
  `value` varchar(1000) NOT NULL,
  `options` varchar(255) NOT NULL,
  `config_id` int NOT NULL,
  `type` varchar(150) NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_config_data`
--

LOCK TABLES `django_config_data` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
INSERT INTO `django_content_type` VALUES (18,'ad','ad'),(17,'ad_sort','adsort'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'captcha','captchastore'),(13,'city','city'),(26,'config','config'),(27,'config_data','configdata'),(5,'contenttypes','contenttype'),(10,'dept','dept'),(24,'dict','dict'),(25,'dict_data','dictdata'),(14,'item','item'),(15,'item_cate','itemcate'),(8,'level','level'),(16,'link','link'),(30,'maochang','eyeglassframecolortype'),(35,'maochang','eyeglassframedetectionresult'),(32,'maochang','eyeglassframeentry'),(34,'maochang','eyeglassframeentrystyle'),(29,'maochang','eyeglassframematerialtype'),(36,'maochang','eyeglassframerecommandationrequest'),(31,'maochang','eyeglassframeshapetype'),(33,'maochang','eyeglassframestyletype'),(23,'member','member'),(22,'member_level','memberlevel'),(28,'menu','menu'),(19,'notice','notice'),(9,'position','position'),(11,'role','role'),(12,'role_menu','rolemenu'),(6,'sessions','session'),(20,'user','user'),(21,'user_role','userrole');
UNLOCK TABLES;

--
-- Table structure for table `django_dept`
--

DROP TABLE IF EXISTS `django_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_dept` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `code` varchar(150) NOT NULL,
  `type` int NOT NULL,
  `pid` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_dept`
--

LOCK TABLES `django_dept` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_dict`
--

DROP TABLE IF EXISTS `django_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_dict` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `code` varchar(150) NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_dict`
--

LOCK TABLES `django_dict` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_dict_data`
--

DROP TABLE IF EXISTS `django_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_dict_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `value` varchar(150) NOT NULL,
  `dict_id` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_dict_data`
--

LOCK TABLES `django_dict_data` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_item`
--

DROP TABLE IF EXISTS `django_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `type` int NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `status` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_item`
--

LOCK TABLES `django_item` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_item_cate`
--

DROP TABLE IF EXISTS `django_item_cate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_item_cate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `pid` int NOT NULL,
  `item_id` int NOT NULL,
  `pinyin` varchar(150) NOT NULL,
  `code` varchar(150) NOT NULL,
  `is_cover` int NOT NULL,
  `cover` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_item_cate`
--

LOCK TABLES `django_item_cate` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_level`
--

DROP TABLE IF EXISTS `django_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `sort` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_level`
--

LOCK TABLES `django_level` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_link`
--

DROP TABLE IF EXISTS `django_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_link` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` int NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `item_id` int NOT NULL,
  `cate_id` int NOT NULL,
  `platform` int NOT NULL,
  `form` int NOT NULL,
  `image` varchar(255) NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_link`
--

LOCK TABLES `django_link` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_member`
--

DROP TABLE IF EXISTS `django_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `realname` varchar(150) NOT NULL,
  `nickname` varchar(150) NOT NULL,
  `gender` int NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `birthday` date NOT NULL,
  `email` varchar(50) NOT NULL,
  `province_code` varchar(30) NOT NULL,
  `city_code` varchar(30) NOT NULL,
  `district_code` varchar(30) NOT NULL,
  `address_info` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `member_level` int NOT NULL,
  `intro` varchar(255) DEFAULT NULL,
  `signature` varchar(255) DEFAULT NULL,
  `source` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_member`
--

LOCK TABLES `django_member` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_member_level`
--

DROP TABLE IF EXISTS `django_member_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_member_level` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_member_level`
--

LOCK TABLES `django_member_level` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_menu`
--

DROP TABLE IF EXISTS `django_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_menu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(150) NOT NULL,
  `icon` varchar(50) NOT NULL,
  `parent_id` int NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  `component` varchar(255) DEFAULT NULL,
  `target` varchar(30) NOT NULL,
  `permission` varchar(150) NOT NULL,
  `type` int NOT NULL,
  `status` int NOT NULL,
  `hide` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_menu`
--

LOCK TABLES `django_menu` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
INSERT INTO `django_migrations` VALUES (1,'ad','0001_initial','2024-04-19 20:56:49.718504'),(2,'ad_sort','0001_initial','2024-04-19 20:56:49.755514'),(3,'contenttypes','0001_initial','2024-04-19 20:56:49.814682'),(4,'auth','0001_initial','2024-04-19 20:56:50.703029'),(5,'admin','0001_initial','2024-04-19 20:56:50.885854'),(6,'admin','0002_logentry_remove_auto_add','2024-04-19 20:56:50.895365'),(7,'admin','0003_logentry_add_action_flag_choices','2024-04-19 20:56:50.905371'),(8,'contenttypes','0002_remove_content_type_name','2024-04-19 20:56:51.048443'),(9,'auth','0002_alter_permission_name_max_length','2024-04-19 20:56:51.141204'),(10,'auth','0003_alter_user_email_max_length','2024-04-19 20:56:51.166275'),(11,'auth','0004_alter_user_username_opts','2024-04-19 20:56:51.175782'),(12,'auth','0005_alter_user_last_login_null','2024-04-19 20:56:51.241469'),(13,'auth','0006_require_contenttypes_0002','2024-04-19 20:56:51.245095'),(14,'auth','0007_alter_validators_add_error_messages','2024-04-19 20:56:51.253987'),(15,'auth','0008_alter_user_username_max_length','2024-04-19 20:56:51.328098'),(16,'auth','0009_alter_user_last_name_max_length','2024-04-19 20:56:51.396167'),(17,'auth','0010_alter_group_name_max_length','2024-04-19 20:56:51.415706'),(18,'auth','0011_update_proxy_permissions','2024-04-19 20:56:51.428195'),(19,'auth','0012_alter_user_first_name_max_length','2024-04-19 20:56:51.499340'),(20,'captcha','0001_initial','2024-04-19 20:56:51.531539'),(21,'captcha','0002_alter_captchastore_id','2024-04-19 20:56:51.643537'),(22,'city','0001_initial','2024-04-19 20:56:51.673546'),(23,'config','0001_initial','2024-04-19 20:56:51.703309'),(24,'config_data','0001_initial','2024-04-19 20:56:51.734575'),(25,'dept','0001_initial','2024-04-19 20:56:51.764268'),(26,'dict','0001_initial','2024-04-19 20:56:51.791303'),(27,'dict_data','0001_initial','2024-04-19 20:56:51.819324'),(28,'item','0001_initial','2024-04-19 20:56:51.848887'),(29,'item_cate','0001_initial','2024-04-19 20:56:51.878992'),(30,'level','0001_initial','2024-04-19 20:56:51.907485'),(31,'link','0001_initial','2024-04-19 20:56:51.935505'),(32,'member','0001_initial','2024-04-19 20:56:51.970097'),(33,'member_level','0001_initial','2024-04-19 20:56:52.000125'),(34,'menu','0001_initial','2024-04-19 20:56:52.035176'),(35,'notice','0001_initial','2024-04-19 20:56:52.067858'),(36,'position','0001_initial','2024-04-19 20:56:52.102443'),(37,'role','0001_initial','2024-04-19 20:56:52.136552'),(38,'role_menu','0001_initial','2024-04-19 20:56:52.171090'),(39,'role_menu','0002_remove_rolemenu_create_time_and_more','2024-04-19 20:56:52.466179'),(40,'sessions','0001_initial','2024-04-19 20:56:52.516528'),(41,'user','0001_initial','2024-04-19 20:56:52.550658'),(42,'user','0002_alter_user_salt','2024-04-19 20:56:52.614708'),(43,'user','0003_alter_user_password','2024-04-19 20:56:52.668332'),(44,'user_role','0001_initial','2024-04-19 20:56:52.699451'),(45,'maochang','0001_initial','2024-04-19 20:58:11.445714'),(46,'maochang','0002_eyeglassframedetectionresult_pile_distance','2024-04-22 20:12:36.979740');
UNLOCK TABLES;

--
-- Table structure for table `django_notice`
--

DROP TABLE IF EXISTS `django_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_notice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(255) NOT NULL,
  `source` int NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `click` int NOT NULL,
  `status` int NOT NULL,
  `is_top` int NOT NULL,
  `content` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_notice`
--

LOCK TABLES `django_notice` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_position`
--

DROP TABLE IF EXISTS `django_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_position` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `sort` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_position`
--

LOCK TABLES `django_position` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_role`
--

DROP TABLE IF EXISTS `django_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) NOT NULL,
  `code` varchar(30) NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_role`
--

LOCK TABLES `django_role` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_role_menu`
--

DROP TABLE IF EXISTS `django_role_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_role_menu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `menu_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_role_menu`
--

LOCK TABLES `django_role_menu` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_user`
--

DROP TABLE IF EXISTS `django_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `realname` varchar(150) NOT NULL,
  `nickname` varchar(150) NOT NULL,
  `gender` int NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `mobile` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `birthday` date NOT NULL,
  `dept_id` int NOT NULL,
  `level_id` int NOT NULL,
  `position_id` int NOT NULL,
  `province_code` varchar(30) NOT NULL,
  `city_code` varchar(30) NOT NULL,
  `district_code` varchar(30) NOT NULL,
  `address_info` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `salt` varchar(30) DEFAULT NULL,
  `intro` varchar(255) DEFAULT NULL,
  `status` int NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_user`
--

LOCK TABLES `django_user` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `django_user_role`
--

DROP TABLE IF EXISTS `django_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_user_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_user_role`
--

LOCK TABLES `django_user_role` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframecolortype`
--

DROP TABLE IF EXISTS `maochang_eyeglassframecolortype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframecolortype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `color` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `color` (`color`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframecolortype`
--

LOCK TABLES `maochang_eyeglassframecolortype` WRITE;
INSERT INTO `maochang_eyeglassframecolortype` VALUES (1,0,'2024-04-19 21:01:21.001422',0,'2024-04-19 21:01:21.001422',0,'玳瑁色'),(2,0,'2024-04-19 21:01:31.511482',0,'2024-04-19 21:01:31.511482',0,'双色'),(3,0,'2024-04-19 21:01:37.804140',0,'2024-04-19 21:01:37.804140',0,'多彩'),(4,0,'2024-04-19 21:04:06.157107',0,'2024-04-19 21:04:06.157107',0,'深色或浅色');
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframedetectionresult`
--

DROP TABLE IF EXISTS `maochang_eyeglassframedetectionresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframedetectionresult` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `frontview` varchar(100) NOT NULL,
  `sideview` varchar(100) NOT NULL,
  `topview` varchar(100) NOT NULL,
  `frontview_bg` varchar(100) NOT NULL,
  `sideview_bg` varchar(100) NOT NULL,
  `topview_bg` varchar(100) NOT NULL,
  `frame_height` decimal(15,4) NOT NULL,
  `frame_width` decimal(15,4) NOT NULL,
  `pile_height_left` decimal(15,4) NOT NULL,
  `pile_height_right` decimal(15,4) NOT NULL,
  `frame_top_width` decimal(15,4) NOT NULL,
  `top_points` varchar(255) NOT NULL,
  `frame_rects` varchar(255) NOT NULL,
  `lens_width_left` decimal(15,4) NOT NULL,
  `lens_width_right` decimal(15,4) NOT NULL,
  `lens_height_left` decimal(15,4) NOT NULL,
  `lens_height_right` decimal(15,4) NOT NULL,
  `lens_diagonal_left` decimal(15,4) NOT NULL,
  `lens_diagonal_right` decimal(15,4) NOT NULL,
  `lens_area_left` decimal(15,4) NOT NULL,
  `lens_area_right` decimal(15,4) NOT NULL,
  `bridge_width` decimal(15,4) NOT NULL,
  `lens_center_points` varchar(255) NOT NULL,
  `lens_top_points` varchar(255) NOT NULL,
  `vertical_angle` decimal(15,4) NOT NULL,
  `forward_angle` decimal(15,4) NOT NULL,
  `temple_angle` decimal(15,4) NOT NULL,
  `drop_length` decimal(15,4) NOT NULL,
  `face_angle` decimal(15,4) NOT NULL,
  `sagittal_angle_left` decimal(15,4) NOT NULL,
  `sagittal_angle_right` decimal(15,4) NOT NULL,
  `temple_length_left` decimal(15,4) NOT NULL,
  `temple_length_right` decimal(15,4) NOT NULL,
  `temporal_width` decimal(15,4) NOT NULL,
  `spread_angle_left` decimal(15,4) NOT NULL,
  `spread_angle_right` decimal(15,4) NOT NULL,
  `weight` decimal(15,4) NOT NULL,
  `entry_id` int NOT NULL,
  `pile_distance` decimal(15,4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entry_id` (`entry_id`),
  CONSTRAINT `maochang_eyeglassfra_entry_id_00d3eb8c_fk_maochang_` FOREIGN KEY (`entry_id`) REFERENCES `maochang_eyeglassframeentry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframedetectionresult`
--

LOCK TABLES `maochang_eyeglassframedetectionresult` WRITE;
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (14,0,'2024-04-22 20:17:08.945021',0,'2024-04-23 23:32:09.274272',0,'images/eyeglassframe/14_0.jpg','images/eyeglassframe/14_1.jpg','images/eyeglassframe/14_2.jpg','images/eyeglassframe/14_0_bg.jpg','images/eyeglassframe/14_1_bg.jpg','images/eyeglassframe/14_2_bg.jpg',11111111111.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1','-1,-1,-1,-1,-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1,-1,-1,-1','-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,0.0000,14,-1.0000),(15,0,'2024-04-22 20:18:08.171358',0,'2024-04-22 20:18:08.171358',0,'images/eyeglassframe/145_0.jpg','images/eyeglassframe/145_1.jpg','images/eyeglassframe/145_2.jpg','images/eyeglassframe/145_0_bg.jpg','images/eyeglassframe/145_1_bg.jpg','images/eyeglassframe/145_2_bg.jpg',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1','-1,-1,-1,-1,-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1,-1,-1,-1','-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,0.0000,15,-1.0000),(16,0,'2024-04-22 20:18:27.487406',0,'2024-04-22 20:18:27.487406',0,'images/eyeglassframe/4678_0.jpg','images/eyeglassframe/4678_1.jpg','images/eyeglassframe/4678_2.jpg','images/eyeglassframe/4678_0_bg.jpg','images/eyeglassframe/4678_1_bg.jpg','images/eyeglassframe/4678_2_bg.jpg',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1','-1,-1,-1,-1,-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1,-1,-1,-1','-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,0.0000,16,-1.0000),(19,0,'2024-04-22 20:59:57.762827',0,'2024-04-22 20:59:57.762827',0,'images/eyeglassframe/test_0.jpg','images/eyeglassframe/test_1.jpg','images/eyeglassframe/test_2.jpg','images/eyeglassframe/test_0_bg.jpg','images/eyeglassframe/test_1_bg.jpg','images/eyeglassframe/test_2_bg.jpg',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1','-1,-1,-1,-1,-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1,-1,-1,-1','-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,0.0000,19,-1.0000),(20,0,'2024-04-22 21:02:18.922287',0,'2024-04-22 21:02:18.922287',0,'images/eyeglassframe/14234_0.jpg','images/eyeglassframe/14234_1.jpg','images/eyeglassframe/14234_2.jpg','images/eyeglassframe/14234_0_bg.jpg','images/eyeglassframe/14234_1_bg.jpg','images/eyeglassframe/14234_2_bg.jpg',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1','-1,-1,-1,-1,-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,'-1,-1,-1,-1','-1,-1,-1,-1',-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,-1.0000,28.1000,20,-1.0000),(21,0,'2024-04-22 21:03:51.696151',0,'2024-04-22 21:03:51.696151',0,'images/eyeglassframe/12356_0.jpg','images/eyeglassframe/12356_1.jpg','images/eyeglassframe/12356_2.jpg','images/eyeglassframe/12356_0_bg.jpg','images/eyeglassframe/12356_1_bg.jpg','images/eyeglassframe/12356_2_bg.jpg',29.8507,136.4341,331.0000,334.0000,2.9184,'887,298,2202,296','406,354,962,491,1713,354,979,492',50.7343,51.6308,24.4279,24.4776,50.7506,51.6505,1048.5720,1082.7522,18.1947,'887,599.5,2202.5,600','783,354,2222,354',19.5751,10.9005,79.0995,56.2724,1.4948,21.1412,23.1165,141.5649,140.6221,137.7211,0.7011,-0.0800,28.2000,21,132.2655);
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframeentry`
--

DROP TABLE IF EXISTS `maochang_eyeglassframeentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframeentry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `sku` varchar(255) NOT NULL,
  `brand` varchar(255) NOT NULL,
  `model_type` varchar(255) NOT NULL,
  `price` decimal(15,2) NOT NULL,
  `isnosepad` tinyint(1) NOT NULL,
  `stock` int DEFAULT NULL,
  `color_id` int NOT NULL,
  `material_id` int NOT NULL,
  `shape_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `maochang_eyeglassfra_material_id_2639c607_fk_maochang_` (`material_id`),
  KEY `maochang_eyeglassfra_shape_id_24e32692_fk_maochang_` (`shape_id`),
  KEY `maochang_eyeglassfra_color_id_44e484e5_fk_maochang_` (`color_id`),
  CONSTRAINT `maochang_eyeglassfra_color_id_44e484e5_fk_maochang_` FOREIGN KEY (`color_id`) REFERENCES `maochang_eyeglassframecolortype` (`id`),
  CONSTRAINT `maochang_eyeglassfra_material_id_2639c607_fk_maochang_` FOREIGN KEY (`material_id`) REFERENCES `maochang_eyeglassframematerialtype` (`id`),
  CONSTRAINT `maochang_eyeglassfra_shape_id_24e32692_fk_maochang_` FOREIGN KEY (`shape_id`) REFERENCES `maochang_eyeglassframeshapetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframeentry`
--

LOCK TABLES `maochang_eyeglassframeentry` WRITE;
INSERT INTO `maochang_eyeglassframeentry` VALUES (14,0,'2024-04-22 20:17:08.937500',0,'2024-04-23 23:32:09.269665',0,'14','16sdfg','111111111111',1.00,1,1,1,7,1),(15,0,'2024-04-22 20:18:08.163844',0,'2024-04-22 20:18:08.163844',0,'145','457','35678',5679.00,1,27,2,2,3),(16,0,'2024-04-22 20:18:27.478902',0,'2024-04-22 20:18:27.478902',0,'4678','1345','3678',589.00,1,25476,4,3,4),(19,0,'2024-04-22 20:59:57.755228',0,'2024-04-22 20:59:57.755228',0,'test','test_brand','test_model_type',1234.00,1,123,2,2,2),(20,0,'2024-04-22 21:02:18.914775',0,'2024-04-22 21:02:18.914775',0,'14234','14','14',1.00,1,1,1,1,1),(21,0,'2024-04-22 21:03:51.689148',0,'2024-04-22 21:03:51.689148',0,'12356','367','245',257.00,1,24578,2,2,2);
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframeentrystyle`
--

DROP TABLE IF EXISTS `maochang_eyeglassframeentrystyle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframeentrystyle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `entry_id` int NOT NULL,
  `style_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `maochang_eyeglassfra_entry_id_aed3827e_fk_maochang_` (`entry_id`),
  KEY `maochang_eyeglassfra_style_id_345b240a_fk_maochang_` (`style_id`),
  CONSTRAINT `maochang_eyeglassfra_entry_id_aed3827e_fk_maochang_` FOREIGN KEY (`entry_id`) REFERENCES `maochang_eyeglassframeentry` (`id`),
  CONSTRAINT `maochang_eyeglassfra_style_id_345b240a_fk_maochang_` FOREIGN KEY (`style_id`) REFERENCES `maochang_eyeglassframestyletype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframeentrystyle`
--

LOCK TABLES `maochang_eyeglassframeentrystyle` WRITE;
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (15,0,'2024-04-22 20:18:08.209483',0,'2024-04-22 20:18:08.209483',0,15,1),(16,0,'2024-04-22 20:18:27.522222',0,'2024-04-22 20:18:27.522222',0,16,3),(17,0,'2024-04-22 20:18:27.529727',0,'2024-04-22 20:18:27.529727',0,16,1),(21,0,'2024-04-22 20:59:57.784767',0,'2024-04-22 20:59:57.784767',0,19,2),(22,0,'2024-04-22 20:59:57.790769',0,'2024-04-22 20:59:57.790769',0,19,3),(23,0,'2024-04-22 21:02:18.941797',0,'2024-04-22 21:02:18.941797',0,20,1),(24,0,'2024-04-22 21:03:51.733629',0,'2024-04-22 21:03:51.733629',0,21,2),(57,0,'2024-04-23 23:32:09.276065',0,'2024-04-23 23:32:09.276065',0,14,3),(58,0,'2024-04-23 23:32:09.278101',0,'2024-04-23 23:32:09.278101',0,14,4),(59,0,'2024-04-23 23:32:09.279066',0,'2024-04-23 23:32:09.279066',0,14,2);
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframematerialtype`
--

DROP TABLE IF EXISTS `maochang_eyeglassframematerialtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframematerialtype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `material` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `material` (`material`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframematerialtype`
--

LOCK TABLES `maochang_eyeglassframematerialtype` WRITE;
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (1,0,'2024-04-19 21:05:37.634078',0,'2024-04-19 21:05:37.634078',0,'天然材料'),(2,0,'2024-04-19 21:05:43.229611',0,'2024-04-19 21:05:43.229611',0,'贵金属'),(3,0,'2024-04-19 21:05:51.583220',0,'2024-04-19 21:05:51.584221',0,'板材'),(4,0,'2024-04-19 21:06:02.573228',0,'2024-04-19 21:06:02.573228',0,'钢材'),(5,0,'2024-04-19 21:06:08.722060',0,'2024-04-19 21:06:08.722060',0,'钛材'),(6,0,'2024-04-19 21:06:13.501598',0,'2024-04-19 21:06:13.501598',0,'合金'),(7,0,'2024-04-19 21:06:18.435536',0,'2024-04-19 21:06:18.435536',0,'其他材料');
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframerecommandationrequest`
--

DROP TABLE IF EXISTS `maochang_eyeglassframerecommandationrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframerecommandationrequest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `facial_width` decimal(15,4) NOT NULL,
  `nose_width` decimal(15,4) NOT NULL,
  `left_ear_distance` decimal(15,4) NOT NULL,
  `right_ear_distance` decimal(15,4) NOT NULL,
  `iris_center_distance` decimal(15,4) NOT NULL,
  `left_eye_width` decimal(15,4) NOT NULL,
  `right_eye_width` decimal(15,4) NOT NULL,
  `left_eye_height` decimal(15,4) NOT NULL,
  `right_eye_height` decimal(15,4) NOT NULL,
  `inner_eyecorner_distance` decimal(15,4) NOT NULL,
  `outter_eyecorner_distance` decimal(15,4) NOT NULL,
  `face_type` varchar(255) NOT NULL,
  `skin_color` varchar(255) NOT NULL,
  `pupil_distance` decimal(15,4) NOT NULL,
  `myopia_left` bigint NOT NULL,
  `myopia_right` bigint NOT NULL,
  `astigmatism_left` bigint NOT NULL,
  `astigmatism_right` bigint NOT NULL,
  `lens_weight` decimal(15,4) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `age` smallint NOT NULL,
  `career` varchar(255) NOT NULL,
  `price_max` bigint NOT NULL,
  `price_min` bigint NOT NULL,
  `style_list` varchar(255) NOT NULL,
  `brand_list` varchar(255) NOT NULL,
  `material_list` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframerecommandationrequest`
--

LOCK TABLES `maochang_eyeglassframerecommandationrequest` WRITE;
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframeshapetype`
--

DROP TABLE IF EXISTS `maochang_eyeglassframeshapetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframeshapetype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `shape` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shape` (`shape`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframeshapetype`
--

LOCK TABLES `maochang_eyeglassframeshapetype` WRITE;
INSERT INTO `maochang_eyeglassframeshapetype` VALUES (1,0,'2024-04-19 21:04:30.583881',0,'2024-04-19 21:04:30.583881',0,'飞行员系列'),(2,0,'2024-04-19 21:04:36.614504',0,'2024-04-19 21:04:36.614504',0,'异形'),(3,0,'2024-04-19 21:04:42.854004',0,'2024-04-19 21:04:42.854004',0,'圆形或不规则圆形'),(4,0,'2024-04-19 21:04:48.475670',0,'2024-04-19 21:04:48.475670',0,'方形或不规则方形');
UNLOCK TABLES;

--
-- Table structure for table `maochang_eyeglassframestyletype`
--

DROP TABLE IF EXISTS `maochang_eyeglassframestyletype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maochang_eyeglassframestyletype` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `style` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `style` (`style`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maochang_eyeglassframestyletype`
--

LOCK TABLES `maochang_eyeglassframestyletype` WRITE;
INSERT INTO `maochang_eyeglassframestyletype` VALUES (1,0,'2024-04-19 21:06:50.640889',0,'2024-04-19 21:06:50.640889',0,'复古经典风'),(2,0,'2024-04-19 21:06:56.744254',0,'2024-04-19 21:06:56.744254',0,'简约时尚风'),(3,0,'2024-04-19 21:07:02.680595',0,'2024-04-19 21:07:02.680595',0,'运动休闲风'),(4,0,'2024-04-19 21:07:08.001498',0,'2024-04-19 21:07:08.001498',0,'奢华个性风');
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-24  0:44:48
