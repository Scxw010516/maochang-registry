/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80300 (8.3.0)
 Source Host           : localhost:3306
 Source Schema         : antdvue

 Target Server Type    : MySQL
 Target Server Version : 80300 (8.3.0)
 File Encoding         : 65001

 Date: 05/05/2024 23:32:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 173 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add captcha store', 7, 'add_captchastore');
INSERT INTO `auth_permission` VALUES (26, 'Can change captcha store', 7, 'change_captchastore');
INSERT INTO `auth_permission` VALUES (27, 'Can delete captcha store', 7, 'delete_captchastore');
INSERT INTO `auth_permission` VALUES (28, 'Can view captcha store', 7, 'view_captchastore');
INSERT INTO `auth_permission` VALUES (29, 'Can add 职级表', 8, 'add_level');
INSERT INTO `auth_permission` VALUES (30, 'Can change 职级表', 8, 'change_level');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 职级表', 8, 'delete_level');
INSERT INTO `auth_permission` VALUES (32, 'Can view 职级表', 8, 'view_level');
INSERT INTO `auth_permission` VALUES (33, 'Can add 岗位表', 9, 'add_position');
INSERT INTO `auth_permission` VALUES (34, 'Can change 岗位表', 9, 'change_position');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 岗位表', 9, 'delete_position');
INSERT INTO `auth_permission` VALUES (36, 'Can view 岗位表', 9, 'view_position');
INSERT INTO `auth_permission` VALUES (37, 'Can add 部门表', 10, 'add_dept');
INSERT INTO `auth_permission` VALUES (38, 'Can change 部门表', 10, 'change_dept');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 部门表', 10, 'delete_dept');
INSERT INTO `auth_permission` VALUES (40, 'Can view 部门表', 10, 'view_dept');
INSERT INTO `auth_permission` VALUES (41, 'Can add 角色表', 11, 'add_role');
INSERT INTO `auth_permission` VALUES (42, 'Can change 角色表', 11, 'change_role');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 角色表', 11, 'delete_role');
INSERT INTO `auth_permission` VALUES (44, 'Can view 角色表', 11, 'view_role');
INSERT INTO `auth_permission` VALUES (45, 'Can add 角色菜单表', 12, 'add_rolemenu');
INSERT INTO `auth_permission` VALUES (46, 'Can change 角色菜单表', 12, 'change_rolemenu');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 角色菜单表', 12, 'delete_rolemenu');
INSERT INTO `auth_permission` VALUES (48, 'Can view 角色菜单表', 12, 'view_rolemenu');
INSERT INTO `auth_permission` VALUES (49, 'Can add 城市表', 13, 'add_city');
INSERT INTO `auth_permission` VALUES (50, 'Can change 城市表', 13, 'change_city');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 城市表', 13, 'delete_city');
INSERT INTO `auth_permission` VALUES (52, 'Can view 城市表', 13, 'view_city');
INSERT INTO `auth_permission` VALUES (53, 'Can add 站点表', 14, 'add_item');
INSERT INTO `auth_permission` VALUES (54, 'Can change 站点表', 14, 'change_item');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 站点表', 14, 'delete_item');
INSERT INTO `auth_permission` VALUES (56, 'Can view 站点表', 14, 'view_item');
INSERT INTO `auth_permission` VALUES (57, 'Can add 栏目表', 15, 'add_itemcate');
INSERT INTO `auth_permission` VALUES (58, 'Can change 栏目表', 15, 'change_itemcate');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 栏目表', 15, 'delete_itemcate');
INSERT INTO `auth_permission` VALUES (60, 'Can view 栏目表', 15, 'view_itemcate');
INSERT INTO `auth_permission` VALUES (61, 'Can add 友链表', 16, 'add_link');
INSERT INTO `auth_permission` VALUES (62, 'Can change 友链表', 16, 'change_link');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 友链表', 16, 'delete_link');
INSERT INTO `auth_permission` VALUES (64, 'Can view 友链表', 16, 'view_link');
INSERT INTO `auth_permission` VALUES (65, 'Can add 广告位表', 17, 'add_adsort');
INSERT INTO `auth_permission` VALUES (66, 'Can change 广告位表', 17, 'change_adsort');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 广告位表', 17, 'delete_adsort');
INSERT INTO `auth_permission` VALUES (68, 'Can view 广告位表', 17, 'view_adsort');
INSERT INTO `auth_permission` VALUES (69, 'Can add 广告表', 18, 'add_ad');
INSERT INTO `auth_permission` VALUES (70, 'Can change 广告表', 18, 'change_ad');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 广告表', 18, 'delete_ad');
INSERT INTO `auth_permission` VALUES (72, 'Can view 广告表', 18, 'view_ad');
INSERT INTO `auth_permission` VALUES (73, 'Can add 通知公告表', 19, 'add_notice');
INSERT INTO `auth_permission` VALUES (74, 'Can change 通知公告表', 19, 'change_notice');
INSERT INTO `auth_permission` VALUES (75, 'Can delete 通知公告表', 19, 'delete_notice');
INSERT INTO `auth_permission` VALUES (76, 'Can view 通知公告表', 19, 'view_notice');
INSERT INTO `auth_permission` VALUES (77, 'Can add 用户表', 20, 'add_user');
INSERT INTO `auth_permission` VALUES (78, 'Can change 用户表', 20, 'change_user');
INSERT INTO `auth_permission` VALUES (79, 'Can delete 用户表', 20, 'delete_user');
INSERT INTO `auth_permission` VALUES (80, 'Can view 用户表', 20, 'view_user');
INSERT INTO `auth_permission` VALUES (81, 'Can add 用户角色表', 21, 'add_userrole');
INSERT INTO `auth_permission` VALUES (82, 'Can change 用户角色表', 21, 'change_userrole');
INSERT INTO `auth_permission` VALUES (83, 'Can delete 用户角色表', 21, 'delete_userrole');
INSERT INTO `auth_permission` VALUES (84, 'Can view 用户角色表', 21, 'view_userrole');
INSERT INTO `auth_permission` VALUES (85, 'Can add 会员等级表', 22, 'add_memberlevel');
INSERT INTO `auth_permission` VALUES (86, 'Can change 会员等级表', 22, 'change_memberlevel');
INSERT INTO `auth_permission` VALUES (87, 'Can delete 会员等级表', 22, 'delete_memberlevel');
INSERT INTO `auth_permission` VALUES (88, 'Can view 会员等级表', 22, 'view_memberlevel');
INSERT INTO `auth_permission` VALUES (89, 'Can add 会员表', 23, 'add_member');
INSERT INTO `auth_permission` VALUES (90, 'Can change 会员表', 23, 'change_member');
INSERT INTO `auth_permission` VALUES (91, 'Can delete 会员表', 23, 'delete_member');
INSERT INTO `auth_permission` VALUES (92, 'Can view 会员表', 23, 'view_member');
INSERT INTO `auth_permission` VALUES (93, 'Can add 字典表', 24, 'add_dict');
INSERT INTO `auth_permission` VALUES (94, 'Can change 字典表', 24, 'change_dict');
INSERT INTO `auth_permission` VALUES (95, 'Can delete 字典表', 24, 'delete_dict');
INSERT INTO `auth_permission` VALUES (96, 'Can view 字典表', 24, 'view_dict');
INSERT INTO `auth_permission` VALUES (97, 'Can add 字典项表', 25, 'add_dictdata');
INSERT INTO `auth_permission` VALUES (98, 'Can change 字典项表', 25, 'change_dictdata');
INSERT INTO `auth_permission` VALUES (99, 'Can delete 字典项表', 25, 'delete_dictdata');
INSERT INTO `auth_permission` VALUES (100, 'Can view 字典项表', 25, 'view_dictdata');
INSERT INTO `auth_permission` VALUES (101, 'Can add 配置表', 26, 'add_config');
INSERT INTO `auth_permission` VALUES (102, 'Can change 配置表', 26, 'change_config');
INSERT INTO `auth_permission` VALUES (103, 'Can delete 配置表', 26, 'delete_config');
INSERT INTO `auth_permission` VALUES (104, 'Can view 配置表', 26, 'view_config');
INSERT INTO `auth_permission` VALUES (105, 'Can add 配置项表', 27, 'add_configdata');
INSERT INTO `auth_permission` VALUES (106, 'Can change 配置项表', 27, 'change_configdata');
INSERT INTO `auth_permission` VALUES (107, 'Can delete 配置项表', 27, 'delete_configdata');
INSERT INTO `auth_permission` VALUES (108, 'Can view 配置项表', 27, 'view_configdata');
INSERT INTO `auth_permission` VALUES (109, 'Can add 菜单表', 28, 'add_menu');
INSERT INTO `auth_permission` VALUES (110, 'Can change 菜单表', 28, 'change_menu');
INSERT INTO `auth_permission` VALUES (111, 'Can delete 菜单表', 28, 'delete_menu');
INSERT INTO `auth_permission` VALUES (112, 'Can view 菜单表', 28, 'view_menu');
INSERT INTO `auth_permission` VALUES (113, 'Can add eyeglass frame material type', 29, 'add_eyeglassframematerialtype');
INSERT INTO `auth_permission` VALUES (114, 'Can change eyeglass frame material type', 29, 'change_eyeglassframematerialtype');
INSERT INTO `auth_permission` VALUES (115, 'Can delete eyeglass frame material type', 29, 'delete_eyeglassframematerialtype');
INSERT INTO `auth_permission` VALUES (116, 'Can view eyeglass frame material type', 29, 'view_eyeglassframematerialtype');
INSERT INTO `auth_permission` VALUES (117, 'Can add eyeglass frame color type', 30, 'add_eyeglassframecolortype');
INSERT INTO `auth_permission` VALUES (118, 'Can change eyeglass frame color type', 30, 'change_eyeglassframecolortype');
INSERT INTO `auth_permission` VALUES (119, 'Can delete eyeglass frame color type', 30, 'delete_eyeglassframecolortype');
INSERT INTO `auth_permission` VALUES (120, 'Can view eyeglass frame color type', 30, 'view_eyeglassframecolortype');
INSERT INTO `auth_permission` VALUES (121, 'Can add eyeglass frame shape type', 31, 'add_eyeglassframeshapetype');
INSERT INTO `auth_permission` VALUES (122, 'Can change eyeglass frame shape type', 31, 'change_eyeglassframeshapetype');
INSERT INTO `auth_permission` VALUES (123, 'Can delete eyeglass frame shape type', 31, 'delete_eyeglassframeshapetype');
INSERT INTO `auth_permission` VALUES (124, 'Can view eyeglass frame shape type', 31, 'view_eyeglassframeshapetype');
INSERT INTO `auth_permission` VALUES (125, 'Can add eyeglass frame entry', 32, 'add_eyeglassframeentry');
INSERT INTO `auth_permission` VALUES (126, 'Can change eyeglass frame entry', 32, 'change_eyeglassframeentry');
INSERT INTO `auth_permission` VALUES (127, 'Can delete eyeglass frame entry', 32, 'delete_eyeglassframeentry');
INSERT INTO `auth_permission` VALUES (128, 'Can view eyeglass frame entry', 32, 'view_eyeglassframeentry');
INSERT INTO `auth_permission` VALUES (129, 'Can add eyeglass frame style type', 33, 'add_eyeglassframestyletype');
INSERT INTO `auth_permission` VALUES (130, 'Can change eyeglass frame style type', 33, 'change_eyeglassframestyletype');
INSERT INTO `auth_permission` VALUES (131, 'Can delete eyeglass frame style type', 33, 'delete_eyeglassframestyletype');
INSERT INTO `auth_permission` VALUES (132, 'Can view eyeglass frame style type', 33, 'view_eyeglassframestyletype');
INSERT INTO `auth_permission` VALUES (133, 'Can add eyeglass frame entry style', 34, 'add_eyeglassframeentrystyle');
INSERT INTO `auth_permission` VALUES (134, 'Can change eyeglass frame entry style', 34, 'change_eyeglassframeentrystyle');
INSERT INTO `auth_permission` VALUES (135, 'Can delete eyeglass frame entry style', 34, 'delete_eyeglassframeentrystyle');
INSERT INTO `auth_permission` VALUES (136, 'Can view eyeglass frame entry style', 34, 'view_eyeglassframeentrystyle');
INSERT INTO `auth_permission` VALUES (137, 'Can add eyeglass frame detection result', 35, 'add_eyeglassframedetectionresult');
INSERT INTO `auth_permission` VALUES (138, 'Can change eyeglass frame detection result', 35, 'change_eyeglassframedetectionresult');
INSERT INTO `auth_permission` VALUES (139, 'Can delete eyeglass frame detection result', 35, 'delete_eyeglassframedetectionresult');
INSERT INTO `auth_permission` VALUES (140, 'Can view eyeglass frame detection result', 35, 'view_eyeglassframedetectionresult');
INSERT INTO `auth_permission` VALUES (141, 'Can add eyeglass frame recommandation request', 36, 'add_eyeglassframerecommandationrequest');
INSERT INTO `auth_permission` VALUES (142, 'Can change eyeglass frame recommandation request', 36, 'change_eyeglassframerecommandationrequest');
INSERT INTO `auth_permission` VALUES (143, 'Can delete eyeglass frame recommandation request', 36, 'delete_eyeglassframerecommandationrequest');
INSERT INTO `auth_permission` VALUES (144, 'Can view eyeglass frame recommandation request', 36, 'view_eyeglassframerecommandationrequest');
INSERT INTO `auth_permission` VALUES (145, 'Can add eyeglass frame recommendation request', 37, 'add_eyeglassframerecommendationrequest');
INSERT INTO `auth_permission` VALUES (146, 'Can change eyeglass frame recommendation request', 37, 'change_eyeglassframerecommendationrequest');
INSERT INTO `auth_permission` VALUES (147, 'Can delete eyeglass frame recommendation request', 37, 'delete_eyeglassframerecommendationrequest');
INSERT INTO `auth_permission` VALUES (148, 'Can view eyeglass frame recommendation request', 37, 'view_eyeglassframerecommendationrequest');
INSERT INTO `auth_permission` VALUES (149, 'Can add recommendation user', 38, 'add_recommendationuser');
INSERT INTO `auth_permission` VALUES (150, 'Can change recommendation user', 38, 'change_recommendationuser');
INSERT INTO `auth_permission` VALUES (151, 'Can delete recommendation user', 38, 'delete_recommendationuser');
INSERT INTO `auth_permission` VALUES (152, 'Can view recommendation user', 38, 'view_recommendationuser');
INSERT INTO `auth_permission` VALUES (153, 'Can add recommendation user optometry', 39, 'add_recommendationuseroptometry');
INSERT INTO `auth_permission` VALUES (154, 'Can change recommendation user optometry', 39, 'change_recommendationuseroptometry');
INSERT INTO `auth_permission` VALUES (155, 'Can delete recommendation user optometry', 39, 'delete_recommendationuseroptometry');
INSERT INTO `auth_permission` VALUES (156, 'Can view recommendation user optometry', 39, 'view_recommendationuseroptometry');
INSERT INTO `auth_permission` VALUES (157, 'Can add recommendation user lens', 40, 'add_recommendationuserlens');
INSERT INTO `auth_permission` VALUES (158, 'Can change recommendation user lens', 40, 'change_recommendationuserlens');
INSERT INTO `auth_permission` VALUES (159, 'Can delete recommendation user lens', 40, 'delete_recommendationuserlens');
INSERT INTO `auth_permission` VALUES (160, 'Can view recommendation user lens', 40, 'view_recommendationuserlens');
INSERT INTO `auth_permission` VALUES (161, 'Can add recommendation user facial scan result', 41, 'add_recommendationuserfacialscanresult');
INSERT INTO `auth_permission` VALUES (162, 'Can change recommendation user facial scan result', 41, 'change_recommendationuserfacialscanresult');
INSERT INTO `auth_permission` VALUES (163, 'Can delete recommendation user facial scan result', 41, 'delete_recommendationuserfacialscanresult');
INSERT INTO `auth_permission` VALUES (164, 'Can view recommendation user facial scan result', 41, 'view_recommendationuserfacialscanresult');
INSERT INTO `auth_permission` VALUES (165, 'Can add recommendation user facial image', 42, 'add_recommendationuserfacialimage');
INSERT INTO `auth_permission` VALUES (166, 'Can change recommendation user facial image', 42, 'change_recommendationuserfacialimage');
INSERT INTO `auth_permission` VALUES (167, 'Can delete recommendation user facial image', 42, 'delete_recommendationuserfacialimage');
INSERT INTO `auth_permission` VALUES (168, 'Can view recommendation user facial image', 42, 'view_recommendationuserfacialimage');
INSERT INTO `auth_permission` VALUES (169, 'Can add recommendation user base info', 43, 'add_recommendationuserbaseinfo');
INSERT INTO `auth_permission` VALUES (170, 'Can change recommendation user base info', 43, 'change_recommendationuserbaseinfo');
INSERT INTO `auth_permission` VALUES (171, 'Can delete recommendation user base info', 43, 'delete_recommendationuserbaseinfo');
INSERT INTO `auth_permission` VALUES (172, 'Can view recommendation user base info', 43, 'view_recommendationuserbaseinfo');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for captcha_captchastore
-- ----------------------------
DROP TABLE IF EXISTS `captcha_captchastore`;
CREATE TABLE `captcha_captchastore`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `response` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `hashkey` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hashkey`(`hashkey` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of captcha_captchastore
-- ----------------------------

-- ----------------------------
-- Table structure for django_ad
-- ----------------------------
DROP TABLE IF EXISTS `django_ad`;
CREATE TABLE `django_ad`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort_id` int NOT NULL,
  `type` int NOT NULL,
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `width` int NOT NULL,
  `height` int NOT NULL,
  `start_time` datetime(6) NULL DEFAULT NULL,
  `end_time` datetime(6) NULL DEFAULT NULL,
  `click` int NOT NULL,
  `status` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_ad
-- ----------------------------

-- ----------------------------
-- Table structure for django_ad_sort
-- ----------------------------
DROP TABLE IF EXISTS `django_ad_sort`;
CREATE TABLE `django_ad_sort`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `item_id` int NOT NULL,
  `cate_id` int NOT NULL,
  `loc_id` int NOT NULL,
  `platform` int NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_ad_sort
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_city
-- ----------------------------
DROP TABLE IF EXISTS `django_city`;
CREATE TABLE `django_city`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `city_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `area_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `zip_code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `level` int NOT NULL,
  `pid` int NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `short_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `full_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `pinyin` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `lng` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `lat` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_city
-- ----------------------------

-- ----------------------------
-- Table structure for django_config
-- ----------------------------
DROP TABLE IF EXISTS `django_config`;
CREATE TABLE `django_config`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_config
-- ----------------------------

-- ----------------------------
-- Table structure for django_config_data
-- ----------------------------
DROP TABLE IF EXISTS `django_config_data`;
CREATE TABLE `django_config_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `value` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `options` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `config_id` int NOT NULL,
  `type` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_config_data
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (18, 'ad', 'ad');
INSERT INTO `django_content_type` VALUES (17, 'ad_sort', 'adsort');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (7, 'captcha', 'captchastore');
INSERT INTO `django_content_type` VALUES (13, 'city', 'city');
INSERT INTO `django_content_type` VALUES (26, 'config', 'config');
INSERT INTO `django_content_type` VALUES (27, 'config_data', 'configdata');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (10, 'dept', 'dept');
INSERT INTO `django_content_type` VALUES (24, 'dict', 'dict');
INSERT INTO `django_content_type` VALUES (25, 'dict_data', 'dictdata');
INSERT INTO `django_content_type` VALUES (14, 'item', 'item');
INSERT INTO `django_content_type` VALUES (15, 'item_cate', 'itemcate');
INSERT INTO `django_content_type` VALUES (8, 'level', 'level');
INSERT INTO `django_content_type` VALUES (16, 'link', 'link');
INSERT INTO `django_content_type` VALUES (30, 'maochang', 'eyeglassframecolortype');
INSERT INTO `django_content_type` VALUES (35, 'maochang', 'eyeglassframedetectionresult');
INSERT INTO `django_content_type` VALUES (32, 'maochang', 'eyeglassframeentry');
INSERT INTO `django_content_type` VALUES (34, 'maochang', 'eyeglassframeentrystyle');
INSERT INTO `django_content_type` VALUES (29, 'maochang', 'eyeglassframematerialtype');
INSERT INTO `django_content_type` VALUES (36, 'maochang', 'eyeglassframerecommandationrequest');
INSERT INTO `django_content_type` VALUES (37, 'maochang', 'eyeglassframerecommendationrequest');
INSERT INTO `django_content_type` VALUES (31, 'maochang', 'eyeglassframeshapetype');
INSERT INTO `django_content_type` VALUES (33, 'maochang', 'eyeglassframestyletype');
INSERT INTO `django_content_type` VALUES (38, 'maochang', 'recommendationuser');
INSERT INTO `django_content_type` VALUES (43, 'maochang', 'recommendationuserbaseinfo');
INSERT INTO `django_content_type` VALUES (42, 'maochang', 'recommendationuserfacialimage');
INSERT INTO `django_content_type` VALUES (41, 'maochang', 'recommendationuserfacialscanresult');
INSERT INTO `django_content_type` VALUES (40, 'maochang', 'recommendationuserlens');
INSERT INTO `django_content_type` VALUES (39, 'maochang', 'recommendationuseroptometry');
INSERT INTO `django_content_type` VALUES (23, 'member', 'member');
INSERT INTO `django_content_type` VALUES (22, 'member_level', 'memberlevel');
INSERT INTO `django_content_type` VALUES (28, 'menu', 'menu');
INSERT INTO `django_content_type` VALUES (19, 'notice', 'notice');
INSERT INTO `django_content_type` VALUES (9, 'position', 'position');
INSERT INTO `django_content_type` VALUES (11, 'role', 'role');
INSERT INTO `django_content_type` VALUES (12, 'role_menu', 'rolemenu');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (20, 'user', 'user');
INSERT INTO `django_content_type` VALUES (21, 'user_role', 'userrole');

-- ----------------------------
-- Table structure for django_dept
-- ----------------------------
DROP TABLE IF EXISTS `django_dept`;
CREATE TABLE `django_dept`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL,
  `pid` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_dept
-- ----------------------------

-- ----------------------------
-- Table structure for django_dict
-- ----------------------------
DROP TABLE IF EXISTS `django_dict`;
CREATE TABLE `django_dict`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_dict
-- ----------------------------

-- ----------------------------
-- Table structure for django_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `django_dict_data`;
CREATE TABLE `django_dict_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `value` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dict_id` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_dict_data
-- ----------------------------

-- ----------------------------
-- Table structure for django_item
-- ----------------------------
DROP TABLE IF EXISTS `django_item`;
CREATE TABLE `django_item`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_item
-- ----------------------------

-- ----------------------------
-- Table structure for django_item_cate
-- ----------------------------
DROP TABLE IF EXISTS `django_item_cate`;
CREATE TABLE `django_item_cate`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `pid` int NOT NULL,
  `item_id` int NOT NULL,
  `pinyin` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_cover` int NOT NULL,
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_item_cate
-- ----------------------------

-- ----------------------------
-- Table structure for django_level
-- ----------------------------
DROP TABLE IF EXISTS `django_level`;
CREATE TABLE `django_level`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_level
-- ----------------------------

-- ----------------------------
-- Table structure for django_link
-- ----------------------------
DROP TABLE IF EXISTS `django_link`;
CREATE TABLE `django_link`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `item_id` int NOT NULL,
  `cate_id` int NOT NULL,
  `platform` int NOT NULL,
  `form` int NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_link
-- ----------------------------

-- ----------------------------
-- Table structure for django_member
-- ----------------------------
DROP TABLE IF EXISTS `django_member`;
CREATE TABLE `django_member`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `realname` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nickname` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` int NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `birthday` date NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `province_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `city_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `district_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `member_level` int NOT NULL,
  `intro` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `signature` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `source` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_member
-- ----------------------------

-- ----------------------------
-- Table structure for django_member_level
-- ----------------------------
DROP TABLE IF EXISTS `django_member_level`;
CREATE TABLE `django_member_level`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_member_level
-- ----------------------------

-- ----------------------------
-- Table structure for django_menu
-- ----------------------------
DROP TABLE IF EXISTS `django_menu`;
CREATE TABLE `django_menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parent_id` int NOT NULL,
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `target` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `permission` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `type` int NOT NULL,
  `status` int NOT NULL,
  `hide` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_menu
-- ----------------------------

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 48 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'ad', '0001_initial', '2024-04-19 20:56:49.718504');
INSERT INTO `django_migrations` VALUES (2, 'ad_sort', '0001_initial', '2024-04-19 20:56:49.755514');
INSERT INTO `django_migrations` VALUES (3, 'contenttypes', '0001_initial', '2024-04-19 20:56:49.814682');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0001_initial', '2024-04-19 20:56:50.703029');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0001_initial', '2024-04-19 20:56:50.885854');
INSERT INTO `django_migrations` VALUES (6, 'admin', '0002_logentry_remove_auto_add', '2024-04-19 20:56:50.895365');
INSERT INTO `django_migrations` VALUES (7, 'admin', '0003_logentry_add_action_flag_choices', '2024-04-19 20:56:50.905371');
INSERT INTO `django_migrations` VALUES (8, 'contenttypes', '0002_remove_content_type_name', '2024-04-19 20:56:51.048443');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0002_alter_permission_name_max_length', '2024-04-19 20:56:51.141204');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0003_alter_user_email_max_length', '2024-04-19 20:56:51.166275');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0004_alter_user_username_opts', '2024-04-19 20:56:51.175782');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0005_alter_user_last_login_null', '2024-04-19 20:56:51.241469');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0006_require_contenttypes_0002', '2024-04-19 20:56:51.245095');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0007_alter_validators_add_error_messages', '2024-04-19 20:56:51.253987');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0008_alter_user_username_max_length', '2024-04-19 20:56:51.328098');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0009_alter_user_last_name_max_length', '2024-04-19 20:56:51.396167');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0010_alter_group_name_max_length', '2024-04-19 20:56:51.415706');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0011_update_proxy_permissions', '2024-04-19 20:56:51.428195');
INSERT INTO `django_migrations` VALUES (19, 'auth', '0012_alter_user_first_name_max_length', '2024-04-19 20:56:51.499340');
INSERT INTO `django_migrations` VALUES (20, 'captcha', '0001_initial', '2024-04-19 20:56:51.531539');
INSERT INTO `django_migrations` VALUES (21, 'captcha', '0002_alter_captchastore_id', '2024-04-19 20:56:51.643537');
INSERT INTO `django_migrations` VALUES (22, 'city', '0001_initial', '2024-04-19 20:56:51.673546');
INSERT INTO `django_migrations` VALUES (23, 'config', '0001_initial', '2024-04-19 20:56:51.703309');
INSERT INTO `django_migrations` VALUES (24, 'config_data', '0001_initial', '2024-04-19 20:56:51.734575');
INSERT INTO `django_migrations` VALUES (25, 'dept', '0001_initial', '2024-04-19 20:56:51.764268');
INSERT INTO `django_migrations` VALUES (26, 'dict', '0001_initial', '2024-04-19 20:56:51.791303');
INSERT INTO `django_migrations` VALUES (27, 'dict_data', '0001_initial', '2024-04-19 20:56:51.819324');
INSERT INTO `django_migrations` VALUES (28, 'item', '0001_initial', '2024-04-19 20:56:51.848887');
INSERT INTO `django_migrations` VALUES (29, 'item_cate', '0001_initial', '2024-04-19 20:56:51.878992');
INSERT INTO `django_migrations` VALUES (30, 'level', '0001_initial', '2024-04-19 20:56:51.907485');
INSERT INTO `django_migrations` VALUES (31, 'link', '0001_initial', '2024-04-19 20:56:51.935505');
INSERT INTO `django_migrations` VALUES (32, 'member', '0001_initial', '2024-04-19 20:56:51.970097');
INSERT INTO `django_migrations` VALUES (33, 'member_level', '0001_initial', '2024-04-19 20:56:52.000125');
INSERT INTO `django_migrations` VALUES (34, 'menu', '0001_initial', '2024-04-19 20:56:52.035176');
INSERT INTO `django_migrations` VALUES (35, 'notice', '0001_initial', '2024-04-19 20:56:52.067858');
INSERT INTO `django_migrations` VALUES (36, 'position', '0001_initial', '2024-04-19 20:56:52.102443');
INSERT INTO `django_migrations` VALUES (37, 'role', '0001_initial', '2024-04-19 20:56:52.136552');
INSERT INTO `django_migrations` VALUES (38, 'role_menu', '0001_initial', '2024-04-19 20:56:52.171090');
INSERT INTO `django_migrations` VALUES (39, 'role_menu', '0002_remove_rolemenu_create_time_and_more', '2024-04-19 20:56:52.466179');
INSERT INTO `django_migrations` VALUES (40, 'sessions', '0001_initial', '2024-04-19 20:56:52.516528');
INSERT INTO `django_migrations` VALUES (41, 'user', '0001_initial', '2024-04-19 20:56:52.550658');
INSERT INTO `django_migrations` VALUES (42, 'user', '0002_alter_user_salt', '2024-04-19 20:56:52.614708');
INSERT INTO `django_migrations` VALUES (43, 'user', '0003_alter_user_password', '2024-04-19 20:56:52.668332');
INSERT INTO `django_migrations` VALUES (44, 'user_role', '0001_initial', '2024-04-19 20:56:52.699451');
INSERT INTO `django_migrations` VALUES (47, 'maochang', '0001_initial', '2024-04-30 04:28:32.594580');

-- ----------------------------
-- Table structure for django_notice
-- ----------------------------
DROP TABLE IF EXISTS `django_notice`;
CREATE TABLE `django_notice`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `source` int NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `click` int NOT NULL,
  `status` int NOT NULL,
  `is_top` int NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_notice
-- ----------------------------

-- ----------------------------
-- Table structure for django_position
-- ----------------------------
DROP TABLE IF EXISTS `django_position`;
CREATE TABLE `django_position`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sort` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_position
-- ----------------------------

-- ----------------------------
-- Table structure for django_role
-- ----------------------------
DROP TABLE IF EXISTS `django_role`;
CREATE TABLE `django_role`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `status` int NOT NULL,
  `sort` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_role
-- ----------------------------

-- ----------------------------
-- Table structure for django_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `django_role_menu`;
CREATE TABLE `django_role_menu`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `menu_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_role_menu
-- ----------------------------

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for django_user
-- ----------------------------
DROP TABLE IF EXISTS `django_user`;
CREATE TABLE `django_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `realname` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nickname` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` int NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mobile` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `birthday` date NOT NULL,
  `dept_id` int NOT NULL,
  `level_id` int NOT NULL,
  `position_id` int NOT NULL,
  `province_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `city_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `district_code` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `salt` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `intro` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` int NOT NULL,
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_user
-- ----------------------------

-- ----------------------------
-- Table structure for django_user_role
-- ----------------------------
DROP TABLE IF EXISTS `django_user_role`;
CREATE TABLE `django_user_role`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_user_role
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_eyeglassframecolortype
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframecolortype`;
CREATE TABLE `maochang_eyeglassframecolortype`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `color`(`color` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframecolortype
-- ----------------------------
INSERT INTO `maochang_eyeglassframecolortype` VALUES (1, 0, '2024-04-30 04:31:28.556014', 0, '2024-04-30 04:31:28.556014', 0, '玳瑁色');
INSERT INTO `maochang_eyeglassframecolortype` VALUES (2, 0, '2024-04-30 04:32:24.562605', 0, '2024-04-30 04:32:24.562605', 0, '双色');
INSERT INTO `maochang_eyeglassframecolortype` VALUES (3, 0, '2024-04-30 04:32:28.901240', 0, '2024-04-30 04:32:28.901240', 0, '多彩');
INSERT INTO `maochang_eyeglassframecolortype` VALUES (4, 0, '2024-04-30 04:32:33.407968', 0, '2024-04-30 04:32:33.407968', 0, '深色或浅色');

-- ----------------------------
-- Table structure for maochang_eyeglassframedetectionresult
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframedetectionresult`;
CREATE TABLE `maochang_eyeglassframedetectionresult`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `frontview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sideview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `topview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `frontview_bg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sideview_bg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `topview_bg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `frame_height` decimal(15, 4) NOT NULL,
  `frame_width` decimal(15, 4) NOT NULL,
  `pile_height_left` decimal(15, 4) NOT NULL,
  `pile_height_right` decimal(15, 4) NOT NULL,
  `frame_top_width` decimal(15, 4) NOT NULL,
  `top_points` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `frame_rects` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `lens_width_left` decimal(15, 4) NOT NULL,
  `lens_width_right` decimal(15, 4) NOT NULL,
  `lens_height_left` decimal(15, 4) NOT NULL,
  `lens_height_right` decimal(15, 4) NOT NULL,
  `lens_diagonal_left` decimal(15, 4) NOT NULL,
  `lens_diagonal_right` decimal(15, 4) NOT NULL,
  `lens_area_left` decimal(15, 4) NOT NULL,
  `lens_area_right` decimal(15, 4) NOT NULL,
  `bridge_width` decimal(15, 4) NOT NULL,
  `lens_center_points` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `lens_top_points` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `vertical_angle` decimal(15, 4) NOT NULL,
  `forward_angle` decimal(15, 4) NOT NULL,
  `temple_angle` decimal(15, 4) NOT NULL,
  `drop_length` decimal(15, 4) NOT NULL,
  `face_angle` decimal(15, 4) NOT NULL,
  `sagittal_angle_left` decimal(15, 4) NOT NULL,
  `sagittal_angle_right` decimal(15, 4) NOT NULL,
  `temple_length_left` decimal(15, 4) NOT NULL,
  `temple_length_right` decimal(15, 4) NOT NULL,
  `temporal_width` decimal(15, 4) NOT NULL,
  `spread_angle_left` decimal(15, 4) NOT NULL,
  `spread_angle_right` decimal(15, 4) NOT NULL,
  `pile_distance` decimal(15, 4) NOT NULL,
  `weight` decimal(15, 4) NOT NULL,
  `entry_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `entry_id`(`entry_id` ASC) USING BTREE,
  CONSTRAINT `maochang_eyeglassfra_entry_id_00d3eb8c_fk_maochang_` FOREIGN KEY (`entry_id`) REFERENCES `maochang_eyeglassframeentry` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframedetectionresult
-- ----------------------------
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (20, 0, '2024-05-05 20:50:58.558545', 0, '2024-05-05 20:50:58.558545', 0, 'images/eyeglassframe/shanghaikiss-S3156_1.jpg', 'images/eyeglassframe/shanghaikiss-S3156_2.jpg', 'images/eyeglassframe/shanghaikiss-S3156_0.jpg', 'images/eyeglassframe/shanghaikiss-S3156_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3156_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3156_0_bg.jpg', 45.8209, 140.6531, 23.8806, 24.0299, 1.4687, '862,280,2221,281', '392,309,940,860,1748,310,946,856', 49.5740, 49.8905, 42.7861, 42.5871, 49.8527, 50.0569, 1701.4949, 1701.0344, 21.9391, '862,739,2221,738', '830,309,2216,310', 37.0767, 14.8128, 75.1872, 38.2133, 8.4307, 35.8377, 41.5682, 138.3739, 138.0112, 147.9469, -5.8699, -2.3255, 133.2609, 17.0000, 20);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (21, 0, '2024-05-05 20:55:57.131343', 0, '2024-05-05 20:55:57.131343', 0, 'images/eyeglassframe/wlc60019_1.jpg', 'images/eyeglassframe/wlc60019_2.jpg', 'images/eyeglassframe/wlc60019_0.jpg', 'images/eyeglassframe/wlc60019_1_bg.jpg', 'images/eyeglassframe/wlc60019_2_bg.jpg', 'images/eyeglassframe/wlc60019_0_bg.jpg', 46.0199, 138.1217, 29.5522, 30.0000, 1.7948, '869,279,2218,274', '381,314,977,845,1737,309,963,840', 51.5254, 50.7870, 42.0398, 41.7910, 52.0613, 51.5005, 1716.6814, 1681.5921, 19.9878, '869.5,736.5,2218.5,729', '842,314,2227,309', 43.5185, 14.6474, 75.3526, 37.7311, 14.2848, 41.3054, 47.4567, 125.0296, 124.3044, 140.4770, -6.7122, -5.4555, 134.5219, 14.9000, 21);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (22, 0, '2024-05-05 21:05:23.331963', 0, '2024-05-05 21:05:23.331963', 0, 'images/eyeglassframe/wlc61149_1.jpg', 'images/eyeglassframe/wlc61149_2.jpg', 'images/eyeglassframe/wlc61149_0.jpg', 'images/eyeglassframe/wlc61149_1_bg.jpg', 'images/eyeglassframe/wlc61149_2_bg.jpg', 'images/eyeglassframe/wlc61149_0_bg.jpg', 47.6617, 147.3509, 34.4279, 35.5721, 2.1740, '826,266,2238,268', '331,309,990,883,1741,311,994,881', 52.2110, 52.4219, 43.9303, 43.8308, 53.4623, 53.5168, 1819.4451, 1823.5094, 22.1501, '826,750.5,2238,751.5', '776,309,2239,311', 38.4992, 18.5923, 71.4077, 33.3154, 6.0198, 42.8278, 42.9581, 136.6333, 138.5189, 152.8059, -3.1818, 0.2856, 138.8356, 18.6000, 22);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (23, 0, '2024-05-05 21:09:59.386038', 0, '2024-05-05 21:09:59.386038', 0, 'images/eyeglassframe/butterfly3124_1.jpg', 'images/eyeglassframe/butterfly3124_2.jpg', 'images/eyeglassframe/butterfly3124_0.jpg', 'images/eyeglassframe/butterfly3124_1_bg.jpg', 'images/eyeglassframe/butterfly3124_2_bg.jpg', 'images/eyeglassframe/butterfly3124_0_bg.jpg', 36.8657, 14.3976, 29.7512, 1.1443, 7.2787, '876,285,1519,0', '410,284,932,874,256,257,2526,915', 49.1521, 133.2170, 43.4826, 45.5224, 51.2861, 133.1810, 1712.8612, 5314.7322, 57.2738, '876,721,1519,714.5', '872,284,717,257', -1.0000, -1.0000, -1.0000, -1.0000, 344.0658, -43.2659, -11.5346, 22.4821, 54.6098, 24.4402, 47.5514, 30.6450, 29.3997, 15.6000, 23);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (24, 0, '2024-05-05 21:16:18.837754', 0, '2024-05-05 21:16:18.837754', 0, 'images/eyeglassframe/powell62180_1.jpg', 'images/eyeglassframe/powell62180_2.jpg', 'images/eyeglassframe/powell62180_0.jpg', 'images/eyeglassframe/powell62180_1_bg.jpg', 'images/eyeglassframe/powell62180_2_bg.jpg', 'images/eyeglassframe/powell62180_0_bg.jpg', 42.0398, 131.8458, 28.4577, 19.0050, 0.6655, '870,314,2196,312', '424,326,892,810,1749,325,895,810', 47.0426, 47.2008, 40.2985, 40.2985, 47.7271, 48.0891, 1505.5077, 1505.7478, 22.8357, '870,731,2196.5,730', '849,326,2200,325', 41.1385, 13.1255, 76.8745, 31.3841, 10.3719, 85.4143, 8.1943, 11.7487, 16.3177, 21.6118, 7.4069, 26.5651, 121.3816, 12.1000, 24);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (25, 0, '2024-05-05 21:19:45.079322', 0, '2024-05-05 21:19:45.079322', 0, 'images/eyeglassframe/butterfly3118_1.jpg', 'images/eyeglassframe/butterfly3118_2.jpg', 'images/eyeglassframe/butterfly3118_0.jpg', 'images/eyeglassframe/butterfly3118_1_bg.jpg', 'images/eyeglassframe/butterfly3118_2_bg.jpg', 'images/eyeglassframe/butterfly3118_0_bg.jpg', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1', '-1,-1,-1,-1,-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1,-1,-1,-1', '-1,-1,-1,-1', 23.9267, 14.3227, 75.6773, 29.9331, 345.3923, 79.6387, 83.4956, 8.1951, 8.1951, 34.1583, -67.0308, 55.0493, 49.7074, 15.2000, 25);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (26, 0, '2024-05-05 21:25:25.605058', 0, '2024-05-05 21:25:25.605058', 0, 'images/eyeglassframe/butterfly3123_1.jpg', 'images/eyeglassframe/butterfly3123_2.jpg', 'images/eyeglassframe/butterfly3123_0.jpg', 'images/eyeglassframe/butterfly3123_1_bg.jpg', 'images/eyeglassframe/butterfly3123_2_bg.jpg', 'images/eyeglassframe/butterfly3123_0_bg.jpg', 48.2090, 144.2921, 37.5622, 37.4129, 2.0051, '825,246,2168,248', '339,285,972,901,1686,288,964,893', 51.2617, 50.8398, 44.8259, 44.4279, 53.0964, 52.9660, 1857.6817, 1845.7133, 19.7769, '825,735.5,2168,734.5', '817,285,2152,288', 39.4325, 11.6024, 78.3976, 38.8773, 238.8478, 34.1770, -17.9203, 138.5914, 145.8437, 12.1839, 6.3628, -6.3054, 12.2775, 19.3000, 26);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (27, 0, '2024-05-05 21:31:56.023281', 0, '2024-05-05 21:31:56.023281', 0, 'images/eyeglassframe/shanghaikiss-SDFF9027_1.jpg', 'images/eyeglassframe/shanghaikiss-SDFF9027_2.jpg', 'images/eyeglassframe/shanghaikiss-SDFF9027_0.jpg', 'images/eyeglassframe/shanghaikiss-SDFF9027_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFF9027_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFF9027_0_bg.jpg', 43.5323, 131.3185, 0.0498, 27.8109, 1.0227, '885,304,2151,312', '440,321,890,792,1702,329,899,796', 46.9371, 47.4118, 39.4030, 39.6020, 47.6627, 47.9483, 1468.3206, 1477.1274, 19.6187, '885,717,2151.5,727', '853,321,2134,329', 40.2063, 14.6926, 75.3074, 41.2444, 15.8310, 33.0576, 33.1356, 130.0337, 130.9765, 137.7211, -2.5138, -2.7715, 124.1026, 16.1000, 27);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (28, 0, '2024-05-05 21:38:12.902334', 0, '2024-05-05 21:38:12.902334', 0, 'images/eyeglassframe/butterfly8001_1.jpg', 'images/eyeglassframe/butterfly8001_2.jpg', 'images/eyeglassframe/butterfly8001_0.jpg', 'images/eyeglassframe/butterfly8001_1_bg.jpg', 'images/eyeglassframe/butterfly8001_2_bg.jpg', 'images/eyeglassframe/butterfly8001_0_bg.jpg', 44.3781, 133.6917, 29.0050, 28.7562, 0.9537, '879,273,2176,266', '411,291,937,841,1706,284,941,848', 49.4158, 49.6268, 41.8408, 42.1891, 50.4260, 50.5644, 1663.3567, 1683.1913, 18.8803, '879.5,711.5,2176.5,708', '818,291,2200,284', 36.3784, 15.4279, 74.5721, 37.5247, 10.7674, 31.8233, 40.2448, 134.0225, 132.4270, 141.1297, -2.7714, -4.9632, 126.7572, 16.6000, 28);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (29, 0, '2024-05-05 21:43:00.630509', 0, '2024-05-05 21:43:00.630509', 0, 'images/eyeglassframe/butterfly7151_1.jpg', 'images/eyeglassframe/butterfly7151_2.jpg', 'images/eyeglassframe/butterfly7151_0.jpg', 'images/eyeglassframe/butterfly7151_1_bg.jpg', 'images/eyeglassframe/butterfly7151_2_bg.jpg', 'images/eyeglassframe/butterfly7151_0_bg.jpg', 45.5721, 144.2921, 27.9602, 38.1592, 1.1576, '865,278,2214,269', '271,297,1188,858,1626,289,1177,858', 62.6531, 62.0730, 42.6866, 42.6866, 64.1802, 63.6822, 1999.8916, 1984.9254, 8.8073, '865,726,2214.5,718', '750,297,2288,289', 38.3654, 16.4893, 73.5107, 40.5261, 346.8483, 10.4077, 39.4793, 135.5455, 135.5455, 64.9806, 0.0324, -0.6552, 118.5943, 17.0000, 29);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (30, 0, '2024-05-05 21:46:08.214167', 0, '2024-05-05 21:46:08.214167', 0, 'images/eyeglassframe/butterfly8006_1.jpg', 'images/eyeglassframe/butterfly8006_2.jpg', 'images/eyeglassframe/butterfly8006_0.jpg', 'images/eyeglassframe/butterfly8006_1_bg.jpg', 'images/eyeglassframe/butterfly8006_2_bg.jpg', 'images/eyeglassframe/butterfly8006_0_bg.jpg', 48.3085, 140.3895, 23.4328, 33.6816, 0.7262, '871,256,2237,262', '362,266,1018,943,1733,272,1008,931', 53.6876, 53.1602, 46.9154, 46.3184, 55.7830, 54.9492, 2033.4788, 1981.2469, 18.6166, '871,737.5,2237,737.5', '768,266,2276,272', 41.9377, 13.5607, 76.4393, 39.5633, 13.7346, 24.4690, 39.6556, 131.2666, 135.9081, 150.6302, -0.2046, -5.0261, 134.4555, 18.4000, 30);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (31, 0, '2024-05-05 21:50:13.646517', 0, '2024-05-05 21:50:13.646517', 0, 'images/eyeglassframe/powell61160_1.jpg', 'images/eyeglassframe/powell61160_2.jpg', 'images/eyeglassframe/powell61160_0.jpg', 'images/eyeglassframe/powell61160_1_bg.jpg', 'images/eyeglassframe/powell61160_2_bg.jpg', 'images/eyeglassframe/powell61160_0_bg.jpg', 46.4677, 145.2414, 32.2388, 32.0398, 2.7901, '828,225,2208,232', '358,279,941,808,1740,286,936,802', 49.6268, 49.3631, 40.1990, 39.9005, 51.5191, 51.2316, 1635.1141, 1617.3445, 23.2576, '828.5,683,2208,687', '752,279,2236,286', 29.0948, 18.5442, 71.4558, 38.2056, 10.1935, -43.6570, 32.9299, 66.5036, 144.1757, 74.1185, 54.6287, -2.6447, 136.9110, 15.0000, 31);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (32, 0, '2024-05-05 21:53:26.268762', 0, '2024-05-05 21:53:26.268762', 0, 'images/eyeglassframe/powell62170_1.jpg', 'images/eyeglassframe/powell62170_2.jpg', 'images/eyeglassframe/powell62170_0.jpg', 'images/eyeglassframe/powell62170_1_bg.jpg', 'images/eyeglassframe/powell62170_2_bg.jpg', 'images/eyeglassframe/powell62170_0_bg.jpg', 44.2289, 137.6998, 22.2886, 30.6965, 1.8763, '824,265,2172,264', '337,302,974,821,1684,301,977,821', 51.3671, 51.5254, 40.8458, 40.8458, 53.4617, 53.4464, 1753.1089, 1749.2887, 19.6714, '824,712.5,2172.5,711.5', '847,302,2166,301', 32.4143, 13.7031, 76.2969, 35.5154, 13.5284, 37.4800, 44.7376, 132.2819, 132.2819, 141.3473, -2.6524, -2.9866, 129.8100, 14.4000, 32);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (33, 0, '2024-05-05 21:57:32.595469', 0, '2024-05-05 21:57:32.595469', 0, 'images/eyeglassframe/shanghaikiss-S1152_1.jpg', 'images/eyeglassframe/shanghaikiss-S1152_2.jpg', 'images/eyeglassframe/shanghaikiss-S1152_0.jpg', 'images/eyeglassframe/shanghaikiss-S1152_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-S1152_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-S1152_0_bg.jpg', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1', '-1,-1,-1,-1,-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1,-1,-1,-1', '-1,-1,-1,-1', 31.9209, 16.6691, 73.3309, 33.0481, 322.5484, -44.3166, -6.6021, 40.9755, 88.0429, 27.8488, 51.9270, 11.2817, 58.7330, 13.0000, 33);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (34, 0, '2024-05-05 22:07:48.623781', 0, '2024-05-05 22:07:48.623781', 0, 'images/eyeglassframe/powell_1.jpg', 'images/eyeglassframe/powell_2.jpg', 'images/eyeglassframe/powell_0.jpg', 'images/eyeglassframe/powell_1_bg.jpg', 'images/eyeglassframe/powell_2_bg.jpg', 'images/eyeglassframe/powell_0_bg.jpg', 52.9353, 140.6531, 31.1443, 29.3035, 1.9294, '813,242,2239,160', '285,276,1056,947,1706,199,1066,983', 55.6917, 56.2191, 47.1144, 48.9055, 57.6617, 57.8266, 2184.3813, 2216.2040, 19.2495, '813,749.5,2239,690.5', '851,276,2285,199', 32.7400, 6.3402, 83.6598, 33.0751, 12.3970, 44.8193, 49.7565, 137.7211, 135.4729, 146.7140, -3.5470, -2.7437, 132.5973, 18.5000, 34);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (35, 0, '2024-05-05 22:13:01.741807', 0, '2024-05-05 22:13:01.741807', 0, 'images/eyeglassframe/wlc62111_1.jpg', 'images/eyeglassframe/wlc62111_2.jpg', 'images/eyeglassframe/wlc62111_0.jpg', 'images/eyeglassframe/wlc62111_1_bg.jpg', 'images/eyeglassframe/wlc62111_2_bg.jpg', 'images/eyeglassframe/wlc62111_0_bg.jpg', 32.4378, 134.2718, 3.5323, 16.3184, 1.1235, '837,326,2236,312', '324,347,1027,606,1722,331,1028,616', 54.1623, 54.2150, 30.1493, 30.6468, 55.9454, 55.8919, 1467.5426, 1485.3386, 19.5659, '837.5,650,2236,639', '812,347,2267,331', 33.2786, 6.6524, 83.3476, 37.2931, 23.0600, 32.1868, 37.3210, 132.6445, 131.6292, 140.1869, -2.1923, -0.9473, 129.4781, 14.3000, 35);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (36, 0, '2024-05-05 22:16:05.612007', 0, '2024-05-05 22:16:05.612007', 0, 'images/eyeglassframe/butterfly3125_1.jpg', 'images/eyeglassframe/butterfly3125_2.jpg', 'images/eyeglassframe/butterfly3125_0.jpg', 'images/eyeglassframe/butterfly3125_1_bg.jpg', 'images/eyeglassframe/butterfly3125_2_bg.jpg', 'images/eyeglassframe/butterfly3125_0_bg.jpg', 45.4229, 134.5882, 31.3433, 34.1791, 2.5064, '891,237,2195,236', '422,283,938,819,1729,284,932,819', 49.4686, 49.1521, 40.7463, 40.7463, 50.5522, 50.2644, 1649.4466, 1638.7966, 19.4604, '891,692.5,2195,693.5', '870,283,2160,284', 33.9298, 15.3053, 74.6947, 33.5300, 2.7092, 36.7500, 40.2227, 133.6599, 133.7324, 133.3698, -5.0883, -2.4574, 126.2926, 15.6000, 36);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (37, 0, '2024-05-05 22:20:54.418821', 0, '2024-05-05 22:20:54.418821', 0, 'images/eyeglassframe/shanghaikiss-SDFB9001_1.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9001_2.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9001_0.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9001_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9001_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9001_0_bg.jpg', 39.0547, 153.4158, 25.5721, 28.0597, 1.0085, '819,297,2275,299', '258,314,1122,755,1717,316,1117,752', 59.1724, 58.9087, 37.5622, 37.4129, 61.4836, 61.2957, 1918.2101, 1907.8605, 17.7728, '819,691.5,2275.5,692', '752,314,2351,316', 33.4210, 5.5961, 84.4039, 46.1692, 11.4938, -34.0616, -3.5035, 18.9285, 46.0521, 107.8417, 35.9318, -2.5187, 145.0739, 19.1000, 37);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (38, 0, '2024-05-05 22:24:05.005456', 0, '2024-05-05 22:24:05.005456', 0, 'images/eyeglassframe/shanghaikiss_1.jpg', 'images/eyeglassframe/shanghaikiss_2.jpg', 'images/eyeglassframe/shanghaikiss_0.jpg', 'images/eyeglassframe/shanghaikiss_1_bg.jpg', 'images/eyeglassframe/shanghaikiss_2_bg.jpg', 'images/eyeglassframe/shanghaikiss_0_bg.jpg', 37.0149, 139.0183, 11.7413, 33.8308, 2.3979, '838,371,2224,343', '331,416,1015,660,1704,390,1040,651', 53.5294, 54.8479, 32.8358, 32.3881, 55.1483, 55.5658, 1509.6336, 1521.3384, 18.8803, '838.5,746,2224,715.5', '822,416,2293,390', 39.7610, 9.6808, 80.3192, 30.2687, 11.6020, 45.8814, 41.0233, 132.6445, 131.9918, 144.8284, -2.2572, -3.1631, 133.2609, 15.4000, 38);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (39, 0, '2024-05-05 22:27:07.039060', 0, '2024-05-05 22:27:07.039060', 0, 'images/eyeglassframe/shanghaikiss-S3238_1.jpg', 'images/eyeglassframe/shanghaikiss-S3238_2.jpg', 'images/eyeglassframe/shanghaikiss-S3238_0.jpg', 'images/eyeglassframe/shanghaikiss-S3238_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3238_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3238_0_bg.jpg', 31.7910, 142.2880, 22.6368, 10.6468, 1.1019, '804,322,2213,328', '274,342,1061,604,1678,349,1071,600', 55.9554, 56.4828, 30.0498, 29.8507, 56.3913, 56.7828, 1426.4500, 1426.7649, 18.0892, '804.5,644,2213.5,649', '735,342,2242,349', 30.6266, 9.2436, 80.7564, 34.8421, 12.1859, 34.8579, 41.2916, 134.1675, 132.5720, 142.8703, -1.2264, -7.8703, 136.7783, 17.3000, 39);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (40, 0, '2024-05-05 22:30:15.371232', 0, '2024-05-05 22:30:15.371232', 0, 'images/eyeglassframe/wlc60008_1.jpg', 'images/eyeglassframe/wlc60008_2.jpg', 'images/eyeglassframe/wlc60008_0.jpg', 'images/eyeglassframe/wlc60008_1_bg.jpg', 'images/eyeglassframe/wlc60008_2_bg.jpg', 'images/eyeglassframe/wlc60008_0_bg.jpg', 38.5572, 138.5964, 25.0746, 28.7562, 1.9687, '852,294,2215,292', '349,332,1007,698,1711,331,1009,698', 53.1075, 53.2130, 34.7264, 34.7264, 54.1133, 54.1063, 1538.1517, 1539.3888, 18.7221, '852.5,681,2215.5,680', '796,332,2224,331', 35.6038, 8.2192, 81.7808, 37.0449, 15.1893, 32.3415, 36.1169, 129.3810, 126.6251, 146.7140, -1.6847, -3.7052, 135.3846, 11.7000, 40);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (41, 0, '2024-05-05 22:37:56.049154', 0, '2024-05-05 22:37:56.049154', 0, 'images/eyeglassframe/butterfly6003_1.jpg', 'images/eyeglassframe/butterfly6003_2.jpg', 'images/eyeglassframe/butterfly6003_0.jpg', 'images/eyeglassframe/butterfly6003_1_bg.jpg', 'images/eyeglassframe/butterfly6003_2_bg.jpg', 'images/eyeglassframe/butterfly6003_0_bg.jpg', 39.5522, 141.9189, 30.8955, 35.7214, 2.5057, '844,280,2210,283', '340,328,1008,698,1701,328,1018,701', 53.1602, 53.6876, 34.7264, 34.8756, 54.2326, 54.5097, 1585.2751, 1600.6243, 18.6166, '844,677,2210,678.5', '778,328,2299,328', 37.1386, 10.9284, 79.0716, 31.3801, 3.1128, 50.3505, 46.3887, 137.4311, 138.8815, 145.8437, -5.9417, -4.5582, 136.7783, 15.9000, 41);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (42, 0, '2024-05-05 22:40:02.084747', 0, '2024-05-05 22:40:02.084747', 0, 'images/eyeglassframe/wlc51119_1.jpg', 'images/eyeglassframe/wlc51119_2.jpg', 'images/eyeglassframe/wlc51119_0.jpg', 'images/eyeglassframe/wlc51119_1_bg.jpg', 'images/eyeglassframe/wlc51119_2_bg.jpg', 'images/eyeglassframe/wlc51119_0_bg.jpg', 33.7313, 132.9006, 22.1891, 21.3930, 1.5443, '884,286,2172,299', '392,313,984,613,1681,327,982,614', 51.8945, 51.7890, 30.4975, 30.5473, 51.8447, 51.7837, 1277.6833, 1282.9873, 16.0852, '884,619.5,2172,634', '746,313,2236,327', 34.2810, 12.0948, 77.9052, 33.3912, 13.5559, 35.8666, 38.7705, 130.1062, 126.5526, 141.0572, -2.7567, -2.5226, 129.5445, 14.5000, 42);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (43, 0, '2024-05-05 22:42:04.011652', 0, '2024-05-05 22:42:04.011652', 0, 'images/eyeglassframe/wlc5008_1.jpg', 'images/eyeglassframe/wlc5008_2.jpg', 'images/eyeglassframe/wlc5008_0.jpg', 'images/eyeglassframe/wlc5008_1_bg.jpg', 'images/eyeglassframe/wlc5008_2_bg.jpg', 'images/eyeglassframe/wlc5008_0_bg.jpg', 35.7214, 141.0751, 22.0398, 21.0945, 1.0169, '825,331,2229,339', '291,349,1068,683,1699,358,1060,679', 56.3245, 55.9026, 33.9801, 33.7811, 57.7222, 57.2284, 1657.8520, 1637.3116, 17.9310, '825,690.5,2229,697.5', '690,349,2255,358', 37.4386, 8.9857, 81.0143, 37.0653, 18.3443, 41.1980, 37.8317, 138.6639, 137.3585, 150.9929, -3.1254, -0.7504, 133.9910, 15.1000, 43);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (44, 0, '2024-05-05 22:44:27.479715', 0, '2024-05-05 22:44:27.479715', 0, 'images/eyeglassframe/shanghaikiss-S3228_1.jpg', 'images/eyeglassframe/shanghaikiss-S3228_2.jpg', 'images/eyeglassframe/shanghaikiss-S3228_0.jpg', 'images/eyeglassframe/shanghaikiss-S3228_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3228_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-S3228_0_bg.jpg', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1', '-1,-1,-1,-1,-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1,-1,-1,-1', '-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, 341.9178, 35.3421, 15.6795, 172.2421, 180.2921, 136.3432, 13.0816, -12.0366, 156.8205, 18.6000, 44);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (45, 0, '2024-05-05 22:47:21.292304', 0, '2024-05-05 22:47:21.292304', 0, 'images/eyeglassframe/shanghaikiss-SDFB9005_1.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9005_2.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9005_0.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9005_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9005_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFB9005_0_bg.jpg', 43.1343, 144.1339, 3.5323, 39.1045, 2.0317, '837,355,2237,334', '333,393,1009,788,1731,373,1013,800', 53.2130, 53.4239, 39.2040, 39.8010, 55.1738, 55.5276, 1767.9531, 1796.5315, 20.5152, '837.5,787,2237.5,773', '783,393,2282,373', 30.9638, 12.6077, 77.3923, 36.4661, 5.1417, 33.7613, 43.7508, 142.3626, 141.0572, 148.3820, -4.4180, -4.4908, 135.9819, 18.1000, 45);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (46, 0, '2024-05-05 22:54:01.827746', 0, '2024-05-05 22:54:01.827746', 0, 'images/eyeglassframe/wlc62155_1.jpg', 'images/eyeglassframe/wlc62155_2.jpg', 'images/eyeglassframe/wlc62155_0.jpg', 'images/eyeglassframe/wlc62155_1_bg.jpg', 'images/eyeglassframe/wlc62155_2_bg.jpg', 'images/eyeglassframe/wlc62155_0_bg.jpg', 37.2139, 141.0223, 29.3035, 34.8756, 1.9532, '856,367,2237,350', '336,403,1040,685,1707,389,1060,687', 54.8479, 55.9026, 34.0796, 34.1791, 56.3296, 57.3449, 1601.4377, 1642.2732, 17.4564, '856,745.5,2237,732.5', '764,403,2336,389', 34.1848, 0.2443, 89.7557, 31.0184, 5.6738, 44.6155, 48.8525, 135.4729, 134.8202, 150.7753, -2.4103, -2.5697, 133.9246, 20.1000, 46);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (47, 0, '2024-05-05 22:55:53.464746', 0, '2024-05-05 22:55:53.464746', 0, 'images/eyeglassframe/butterfly2136_1.jpg', 'images/eyeglassframe/butterfly2136_2.jpg', 'images/eyeglassframe/butterfly2136_0.jpg', 'images/eyeglassframe/butterfly2136_1_bg.jpg', 'images/eyeglassframe/butterfly2136_2_bg.jpg', 'images/eyeglassframe/butterfly2136_0_bg.jpg', 37.9602, 128.3651, 25.2239, 24.3284, 0.9958, '900,300,2145,304', '462,318,876,717,1711,322,869,713', 46.1988, 45.8296, 35.6716, 35.4726, 47.5293, 47.3005, 1388.8182, 1375.9708, 19.6714, '900,676.5,2145.5,678.5', '846,318,2170,322', 32.5926, 11.4378, 78.5622, 39.9522, 15.3905, 29.6499, 31.4902, 132.2819, 132.2094, 138.4464, -1.7176, -2.1064, 123.7707, 17.3000, 47);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (48, 0, '2024-05-05 22:59:41.018171', 0, '2024-05-05 22:59:41.018171', 0, 'images/eyeglassframe/butterfly3122_1.jpg', 'images/eyeglassframe/butterfly3122_2.jpg', 'images/eyeglassframe/butterfly3122_0.jpg', 'images/eyeglassframe/butterfly3122_1_bg.jpg', 'images/eyeglassframe/butterfly3122_2_bg.jpg', 'images/eyeglassframe/butterfly3122_0_bg.jpg', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1', '-1,-1,-1,-1,-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1,-1,-1,-1', '-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, 20.4000, 48);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (49, 0, '2024-05-05 23:01:20.714101', 0, '2024-05-05 23:01:20.714101', 0, 'images/eyeglassframe/wlc61148_1.jpg', 'images/eyeglassframe/wlc61148_2.jpg', 'images/eyeglassframe/wlc61148_0.jpg', 'images/eyeglassframe/wlc61148_1_bg.jpg', 'images/eyeglassframe/wlc61148_2_bg.jpg', 'images/eyeglassframe/wlc61148_0_bg.jpg', 46.4677, 151.3063, 26.0697, 36.1692, 2.5565, '815,290,2269,295', '304,340,1023,875,1751,345,1037,879', 53.9513, 54.6897, 43.5323, 43.7313, 56.4788, 56.9847, 1940.4507, 1973.5053, 22.3611, '815.5,777.5,2269.5,784.5', '742,340,2265,345', 34.7252, 14.5824, 75.4176, 38.8289, 5.6767, 36.9222, 37.2190, 138.3739, 139.0991, 154.6915, -2.3156, -1.0336, 141.8884, 19.3000, 49);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (50, 0, '2024-05-05 23:03:22.951648', 0, '2024-05-05 23:03:22.951648', 0, 'images/eyeglassframe/butterfly6002_1.jpg', 'images/eyeglassframe/butterfly6002_2.jpg', 'images/eyeglassframe/butterfly6002_0.jpg', 'images/eyeglassframe/butterfly6002_1_bg.jpg', 'images/eyeglassframe/butterfly6002_2_bg.jpg', 'images/eyeglassframe/butterfly6002_0_bg.jpg', 46.9154, 141.1805, 36.5174, 42.4378, 2.1475, '855,285,2221,283', '338,324,1035,855,1698,322,1046,858', 54.5842, 55.1643, 42.5373, 42.6866, 57.4109, 57.8615, 1927.6400, 1951.3080, 17.1400, '855.5,751.5,2221,751', '756,324,2264,322', 38.6215, 10.7204, 79.2796, 32.1950, 163.7954, -90.0000, 53.9579, -4.4239, -0.2901, 144.1757, -84.0772, -53.3852, 35.4389, 16.7000, 50);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (51, 0, '2024-05-05 23:04:57.234866', 0, '2024-05-05 23:04:57.234866', 0, 'images/eyeglassframe/powell61159_1.jpg', 'images/eyeglassframe/powell61159_2.jpg', 'images/eyeglassframe/powell61159_0.jpg', 'images/eyeglassframe/powell61159_1_bg.jpg', 'images/eyeglassframe/powell61159_2_bg.jpg', 'images/eyeglassframe/powell61159_0_bg.jpg', 44.4279, 147.0345, 31.6418, 36.0199, 2.5721, '848,268,2220,274', '350,318,996,772,1723,324,995,773', 52.5274, 52.4746, 38.4080, 38.4577, 53.5298, 53.6062, 1694.9774, 1694.6743, 19.8824, '848,704,2220.5,710.5', '770,318,2280,324', 32.6353, 17.6958, 72.3042, 33.2548, 0.5573, -41.9817, 44.6116, 60.9918, 131.7017, 155.1992, 50.9096, -1.6215, 136.4465, 14.3000, 51);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (52, 0, '2024-05-05 23:06:44.904455', 0, '2024-05-05 23:06:44.904455', 0, 'images/eyeglassframe/shanghaikiss-S5399_1.jpg', 'images/eyeglassframe/shanghaikiss-S5399_2.jpg', 'images/eyeglassframe/shanghaikiss-S5399_0.jpg', 'images/eyeglassframe/shanghaikiss-S5399_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-S5399_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-S5399_0_bg.jpg', 38.4577, 144.8722, 31.1940, 31.0945, 2.2370, '851,452,2215,458', '393,495,916,665,1758,502,915,666', 48.3083, 48.2556, 33.0846, 33.1343, 48.8103, 48.9026, 1335.0933, 1339.3688, 23.6795, '851,827.5,2215.5,835', '805,495,2202,502', 41.3542, 13.8234, 76.1766, 36.8175, 12.6431, 39.0939, 36.2942, 129.7436, 129.9612, 144.1757, -1.8325, -2.6957, 134.1901, 12.1000, 52);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (53, 0, '2024-05-05 23:08:10.091217', 0, '2024-05-05 23:08:10.091217', 0, 'images/eyeglassframe/butterfly8009_1.jpg', 'images/eyeglassframe/butterfly8009_2.jpg', 'images/eyeglassframe/butterfly8009_0.jpg', 'images/eyeglassframe/butterfly8009_1_bg.jpg', 'images/eyeglassframe/butterfly8009_2_bg.jpg', 'images/eyeglassframe/butterfly8009_0_bg.jpg', 46.2687, 140.2312, 22.8358, 30.0000, 0.9968, '830,280,2201,280', '336,298,988,883,1706,298,990,878', 52.1055, 52.2110, 43.9303, 43.6816, 53.6536, 53.6543, 1886.7455, 1876.7712, 20.1460, '830,739.5,2201,737', '816,298,2180,298', 40.5145, 14.3299, 75.6701, 39.4978, 11.8997, 24.2413, 35.1715, 133.6599, 135.2554, 72.3054, -1.3077, -4.7294, 130.5400, 17.9000, 53);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (54, 0, '2024-05-05 23:10:35.183139', 0, '2024-05-05 23:10:35.183139', 0, 'images/eyeglassframe/powell62172_1.jpg', 'images/eyeglassframe/powell62172_2.jpg', 'images/eyeglassframe/powell62172_0.jpg', 'images/eyeglassframe/powell62172_1_bg.jpg', 'images/eyeglassframe/powell62172_2_bg.jpg', 'images/eyeglassframe/powell62172_0_bg.jpg', 30.7463, 140.9696, 14.4279, 15.1244, 1.2133, '858,344,2221,332', '351,364,1014,575,1713,356,1016,571', 53.4767, 53.5822, 28.6070, 28.4080, 53.9290, 53.9022, 1276.3832, 1245.7163, 18.3529, '858,651.5,2221,641.5', '771,364,2275,356', 33.3885, 10.7510, 79.2490, 31.5023, 25.4350, 41.4354, 43.8309, 127.4229, 124.3769, 142.5077, -5.8175, -3.9619, 136.4465, 13.0000, 54);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (55, 0, '2024-05-05 23:12:03.459591', 0, '2024-05-05 23:12:03.459591', 0, 'images/eyeglassframe/wlc60004_1.jpg', 'images/eyeglassframe/wlc60004_2.jpg', 'images/eyeglassframe/wlc60004_0.jpg', 'images/eyeglassframe/wlc60004_1_bg.jpg', 'images/eyeglassframe/wlc60004_2_bg.jpg', 'images/eyeglassframe/wlc60004_0_bg.jpg', 39.3035, 135.3266, 27.7612, 32.3881, 1.8700, '879,297,2198,299', '395,333,969,717,1708,336,981,715', 51.1034, 51.7363, 35.6716, 35.5721, 51.4880, 52.0234, 1499.8508, 1517.3594, 18.1420, '879.5,691.5,2198.5,693.5', '843,333,2195,336', 80.3112, 25.2517, 64.7483, 5.7379, 358.9736, 12.3080, 16.2602, 16.0276, 16.7528, 9.2829, 61.5661, 63.2270, 103.7285, 11.9000, 55);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (56, 0, '2024-05-05 23:13:32.407240', 0, '2024-05-05 23:13:32.407240', 0, 'images/eyeglassframe/butterfly8014_1.jpg', 'images/eyeglassframe/butterfly8014_2.jpg', 'images/eyeglassframe/butterfly8014_0.jpg', 'images/eyeglassframe/butterfly8014_1_bg.jpg', 'images/eyeglassframe/butterfly8014_2_bg.jpg', 'images/eyeglassframe/butterfly8014_0_bg.jpg', 46.8657, 143.3955, 30.7960, 26.9652, 1.3202, '847,278,2236,279', '347,300,1000,893,1734,299,1005,890', 52.7383, 53.0020, 44.4279, 44.2786, 54.3229, 54.3187, 1937.0687, 1933.4609, 20.4097, '847,746.5,2236.5,744', '793,300,2220,299', 37.9185, 14.6503, 75.3497, 37.1893, 8.3922, 39.4547, 37.1614, 135.6905, 136.7058, 150.1951, -1.4209, -0.5695, 132.0664, 17.8000, 56);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (57, 0, '2024-05-05 23:15:09.680079', 0, '2024-05-05 23:15:09.680079', 0, 'images/eyeglassframe/wlc60014_1.jpg', 'images/eyeglassframe/wlc60014_2.jpg', 'images/eyeglassframe/wlc60014_0.jpg', 'images/eyeglassframe/wlc60014_1_bg.jpg', 'images/eyeglassframe/wlc60014_2_bg.jpg', 'images/eyeglassframe/wlc60014_0_bg.jpg', 38.8557, 134.1663, 11.0945, 11.2438, 1.7544, '845,306,2188,303', '351,341,988,703,1694,337,989,702', 52.1055, 52.1582, 34.9751, 34.9254, 52.9284, 53.0199, 1531.8231, 1532.9408, 18.7221, '845,692.5,2188.5,688', '815,341,2197,337', 41.4419, 8.8129, 81.1871, 44.5351, 16.6885, 28.2800, 34.5599, 128.0031, 126.5526, 143.0153, 3.1489, 0.6483, 131.6682, 13.5000, 57);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (58, 0, '2024-05-05 23:17:38.457638', 0, '2024-05-05 23:17:38.457638', 0, 'images/eyeglassframe/wlc60017_1.jpg', 'images/eyeglassframe/wlc60017_2.jpg', 'images/eyeglassframe/wlc60017_0.jpg', 'images/eyeglassframe/wlc60017_1_bg.jpg', 'images/eyeglassframe/wlc60017_2_bg.jpg', 'images/eyeglassframe/wlc60017_0_bg.jpg', 40.9950, 135.5903, 28.9552, 28.3582, 1.8736, '845,324,2185,326', '376,360,938,741,1714,364,942,745', 49.4686, 49.6795, 36.8657, 37.0647, 50.3488, 50.5287, 1513.3279, 1523.1081, 21.0953, '845,730.5,2185,736.5', '810,360,2151,364', 44.5489, 10.1472, 79.8528, 37.1669, 13.8603, 46.1075, 48.2397, 124.0143, 124.0143, 136.4883, -7.1299, -6.6380, 132.1327, 14.2000, 58);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (59, 0, '2024-05-05 23:19:23.931272', 0, '2024-05-05 23:19:23.931272', 0, 'images/eyeglassframe/wlc62158_1.jpg', 'images/eyeglassframe/wlc62158_2.jpg', 'images/eyeglassframe/wlc62158_0.jpg', 'images/eyeglassframe/wlc62158_1_bg.jpg', 'images/eyeglassframe/wlc62158_2_bg.jpg', 'images/eyeglassframe/wlc62158_0_bg.jpg', 33.3333, 132.2678, 20.1990, 21.2438, 0.9917, '879,304,2194,301', '381,324,997,620,1699,317,990,621', 52.5801, 52.2110, 30.8458, 30.8955, 52.7406, 52.5213, 1312.4145, 1307.6510, 16.9290, '879.5,634,2194,627.5', '825,324,2241,317', 37.8603, 15.5241, 74.4759, 31.3937, 15.8592, -37.0744, 3.9348, 25.7457, 61.4995, 65.4157, 40.6231, 7.5148, 124.8326, 11.9000, 59);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (60, 0, '2024-05-05 23:21:18.107516', 0, '2024-05-05 23:21:18.107516', 0, 'images/eyeglassframe/shanghaikiss-SDFC9005_1.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9005_2.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9005_0.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9005_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9005_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9005_0_bg.jpg', 49.1542, 141.6024, 31.9403, 35.5721, 0.9783, '849,262,2209,229', '345,280,1008,763,1703,245,1012,722', 53.1602, 53.3712, 37.9602, 35.9204, 58.3851, 53.7783, 1679.9102, 1579.2587, 18.4584, '849,661.5,2209,606', '780,280,2285,245', 37.4461, 10.2597, 79.7403, 39.3279, 26.4201, 41.1083, 40.5467, 126.4801, 133.0072, 141.7824, -6.2258, -5.7563, 139.1011, 16.3000, 60);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (61, 0, '2024-05-05 23:23:05.786144', 0, '2024-05-05 23:23:05.786144', 0, 'images/eyeglassframe/butterfly3126_1.jpg', 'images/eyeglassframe/butterfly3126_2.jpg', 'images/eyeglassframe/butterfly3126_0.jpg', 'images/eyeglassframe/butterfly3126_1_bg.jpg', 'images/eyeglassframe/butterfly3126_2_bg.jpg', 'images/eyeglassframe/butterfly3126_0_bg.jpg', 39.0050, 140.3895, 29.6020, 30.3980, 2.3720, '872,294,2195,288', '399,341,947,684,1722,335,946,683', 49.9432, 49.8905, 34.0299, 33.9801, 50.6228, 50.5955, 1401.7102, 1401.6840, 19.8296, '872.5,683,2195,676.5', '837,341,2212,335', 37.6618, 9.8101, 80.1899, 37.9316, 2.3729, 41.2643, 45.8198, 133.1522, 132.2819, 139.8243, -5.9856, -4.9452, 134.5882, 15.3000, 61);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (62, 0, '2024-05-05 23:24:38.760109', 0, '2024-05-05 23:24:38.760109', 0, 'images/eyeglassframe/wlc5010_1.jpg', 'images/eyeglassframe/wlc5010_2.jpg', 'images/eyeglassframe/wlc5010_0.jpg', 'images/eyeglassframe/wlc5010_1_bg.jpg', 'images/eyeglassframe/wlc5010_2_bg.jpg', 'images/eyeglassframe/wlc5010_0_bg.jpg', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1', '-1,-1,-1,-1,-1,-1,-1,-1', -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, -1.0000, '-1,-1,-1,-1', '-1,-1,-1,-1', 38.8549, 11.5700, 78.4300, 37.9692, 17.5144, 3.8785, 6.6625, 87.3177, 87.3177, 144.9734, 5.6010, 3.8899, 129.6772, 15.5000, 62);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (63, 0, '2024-05-05 23:26:46.139579', 0, '2024-05-05 23:26:46.139579', 0, 'images/eyeglassframe/wlc62172_1.jpg', 'images/eyeglassframe/wlc62172_2.jpg', 'images/eyeglassframe/wlc62172_0.jpg', 'images/eyeglassframe/wlc62172_1_bg.jpg', 'images/eyeglassframe/wlc62172_2_bg.jpg', 'images/eyeglassframe/wlc62172_0_bg.jpg', 30.3483, 140.3895, 14.5771, 13.9303, 1.1702, '847,336,2213,337', '336,357,1022,577,1705,359,1017,573', 53.8986, 53.6349, 28.7065, 28.5075, 54.1518, 53.9870, 1269.8959, 1251.9570, 18.3002, '847,645.5,2213.5,645.5', '777,357,2251,359', 34.5994, 9.2673, 80.7327, 31.3400, 26.2257, 42.6141, 44.3305, 125.7549, 125.8274, 143.0153, -3.7763, -3.8353, 136.1810, 13.1000, 63);
INSERT INTO `maochang_eyeglassframedetectionresult` VALUES (64, 0, '2024-05-05 23:28:23.048167', 0, '2024-05-05 23:28:23.048167', 0, 'images/eyeglassframe/shanghaikiss-SDFC9007_1.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9007_2.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9007_0.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9007_1_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9007_2_bg.jpg', 'images/eyeglassframe/shanghaikiss-SDFC9007_0_bg.jpg', 39.4030, 135.5903, 8.3085, 27.5124, 0.6403, '873,314,2155,311', '397,323,953,668,1677,322,956,670', 50.2596, 50.4179, 33.2338, 33.3333, 51.1874, 51.1783, 1368.9482, 1378.0200, 17.2454, '873.5,657,2155,657', '783,323,2226,322', 34.6389, 10.1986, 79.8014, 38.5090, 18.5866, 25.0334, 38.3800, 126.5526, 127.0603, 137.2860, -3.1316, -6.3133, 131.4027, 12.5000, 64);

-- ----------------------------
-- Table structure for maochang_eyeglassframeentry
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframeentry`;
CREATE TABLE `maochang_eyeglassframeentry`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `sku` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `brand` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` decimal(15, 2) NOT NULL,
  `isnosepad` tinyint(1) NOT NULL,
  `stock` int NULL DEFAULT NULL,
  `color_id` int NOT NULL,
  `material_id` int NOT NULL,
  `shape_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `sku`(`sku` ASC) USING BTREE,
  INDEX `maochang_eyeglassfra_material_id_2639c607_fk_maochang_`(`material_id` ASC) USING BTREE,
  INDEX `maochang_eyeglassfra_shape_id_24e32692_fk_maochang_`(`shape_id` ASC) USING BTREE,
  INDEX `maochang_eyeglassfra_color_id_44e484e5_fk_maochang_`(`color_id` ASC) USING BTREE,
  CONSTRAINT `maochang_eyeglassfra_color_id_44e484e5_fk_maochang_` FOREIGN KEY (`color_id`) REFERENCES `maochang_eyeglassframecolortype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `maochang_eyeglassfra_material_id_2639c607_fk_maochang_` FOREIGN KEY (`material_id`) REFERENCES `maochang_eyeglassframematerialtype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `maochang_eyeglassfra_shape_id_24e32692_fk_maochang_` FOREIGN KEY (`shape_id`) REFERENCES `maochang_eyeglassframeshapetype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframeentry
-- ----------------------------
INSERT INTO `maochang_eyeglassframeentry` VALUES (20, 0, '2024-05-05 20:50:58.499424', 0, '2024-05-05 20:50:58.499424', 0, 'shanghaikiss-S3156', '情定上海', 'S3156-C101', 499.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (21, 0, '2024-05-05 20:55:57.127834', 0, '2024-05-05 20:55:57.127834', 0, 'wlc60019', '吴良材', '60019-C13', 299.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (22, 0, '2024-05-05 21:05:23.329963', 0, '2024-05-05 21:05:23.329963', 0, 'wlc61149', '吴良材', '61149-C1M', 699.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (23, 0, '2024-05-05 21:09:59.383036', 0, '2024-05-05 21:09:59.383036', 0, 'butterfly3124', '百特妃兰', '3124-C07', 599.00, 1, 1, 4, 1, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (24, 0, '2024-05-05 21:16:18.834247', 0, '2024-05-05 21:16:18.834247', 0, 'powell62180', '伯韦尔', '62180-C3S', 499.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (25, 0, '2024-05-05 21:19:45.076804', 0, '2024-05-05 21:19:45.076804', 0, 'butterfly3118', '百特妃兰', '3118-C05', 499.00, 1, 1, 4, 7, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (26, 0, '2024-05-05 21:25:25.602555', 0, '2024-05-05 21:25:25.602555', 0, 'butterfly3123', '百特妃兰', '3123-C10', 499.00, 1, 1, 4, 7, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (27, 0, '2024-05-05 21:31:56.019908', 0, '2024-05-05 21:31:56.019908', 0, 'shanghaikiss-SDFF9027', '情定上海', 'SDFF9027', 499.00, 1, 1, 2, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (28, 0, '2024-05-05 21:38:12.898336', 0, '2024-05-05 21:38:12.898336', 0, 'butterfly8001', '百特妃兰', '8001-C01', 299.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (29, 0, '2024-05-05 21:43:00.626611', 0, '2024-05-05 21:43:00.626611', 0, 'butterfly7151', '百特妃兰', '7151-C02', 499.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (30, 0, '2024-05-05 21:46:08.211607', 0, '2024-05-05 21:46:08.211607', 0, 'butterfly8006', '百特妃兰', '8001-C03S', 232.00, 1, 1, 4, 5, 3);
INSERT INTO `maochang_eyeglassframeentry` VALUES (31, 0, '2024-05-05 21:50:13.642494', 0, '2024-05-05 21:50:13.642494', 0, 'powell61160', '伯韦尔', '61160-C3S', 299.00, 1, 1, 2, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (32, 0, '2024-05-05 21:53:26.263706', 0, '2024-05-05 21:53:26.263706', 0, 'powell62170', '伯韦尔', '62170-C25S', 299.00, 1, 1, 4, 4, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (33, 0, '2024-05-05 21:57:32.592530', 0, '2024-05-05 21:57:32.592530', 0, 'shanghaikiss-S1152', '情定上海', 'S1152-C2', 299.00, 1, 1, 2, 5, 1);
INSERT INTO `maochang_eyeglassframeentry` VALUES (34, 0, '2024-05-05 22:07:48.621262', 0, '2024-05-05 22:07:48.621262', 0, 'powell', '伯韦尔', '62175-C25S', 299.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (35, 0, '2024-05-05 22:13:01.738808', 0, '2024-05-05 22:13:01.738808', 0, 'wlc62111', '吴良材', '62111-C2S', 1222.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (36, 0, '2024-05-05 22:16:05.609008', 0, '2024-05-05 22:16:05.609008', 0, 'butterfly3125', '百特妃兰', '3125-C01', 2222.00, 1, 1, 4, 1, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (37, 0, '2024-05-05 22:20:54.416817', 0, '2024-05-05 22:20:54.416817', 0, 'shanghaikiss-SDFB9001', '情定上海', 'SDFB9001-C01', 499.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (38, 0, '2024-05-05 22:24:05.002952', 0, '2024-05-05 22:24:05.002952', 0, 'shanghaikiss', '情定上海', 'S5402-C4', 233.00, 1, 1, 1, 7, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (39, 0, '2024-05-05 22:27:07.035530', 0, '2024-05-05 22:27:07.035530', 0, 'shanghaikiss-S3238', '情定上海', 'S3238-C514', 233.00, 1, 1, 4, 4, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (40, 0, '2024-05-05 22:30:15.368220', 0, '2024-05-05 22:30:15.368220', 0, 'wlc60008', '吴良材', '60008-C1', 211.00, 1, 1, 4, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (41, 0, '2024-05-05 22:37:56.044583', 0, '2024-05-05 22:37:56.044583', 0, 'butterfly6003', '百特妃兰', '6003-C04', 299.00, 1, 1, 4, 1, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (42, 0, '2024-05-05 22:40:02.081264', 0, '2024-05-05 22:40:02.081264', 0, 'wlc51119', '吴良材', '51119-C2S', 112.00, 1, 1, 2, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (43, 0, '2024-05-05 22:42:04.009143', 0, '2024-05-05 22:42:04.009143', 0, 'wlc5008', '吴良材', '5008-C2S', 722.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (44, 0, '2024-05-05 22:44:27.476712', 0, '2024-05-05 22:44:27.476712', 0, 'shanghaikiss-S3228', '情定上海', 'S3228-A24', 23.00, 1, 1, 4, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (45, 0, '2024-05-05 22:47:21.287208', 0, '2024-05-05 22:47:21.287208', 0, 'shanghaikiss-SDFB9005', '情定上海', 'SDFB9005-C02', 1.00, 1, 1, 2, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (46, 0, '2024-05-05 22:54:01.824750', 0, '2024-05-05 22:54:01.824750', 0, 'wlc62155', '吴良材', '62155-C1M', 700.00, 1, 1, 4, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (47, 0, '2024-05-05 22:55:53.462416', 0, '2024-05-05 22:55:53.462416', 0, 'butterfly2136', '百特妃兰', '2136-C15', 11.00, 1, 1, 4, 4, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (48, 0, '2024-05-05 22:59:41.013491', 0, '2024-05-05 22:59:41.013491', 0, 'butterfly3122', '百特妃兰', '3122-C05', 299.00, 1, 1, 4, 7, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (49, 0, '2024-05-05 23:01:20.711102', 0, '2024-05-05 23:01:20.711102', 0, 'wlc61148', '吴良材', '61148-C3S', 299.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (50, 0, '2024-05-05 23:03:22.948652', 0, '2024-05-05 23:03:22.948652', 0, 'butterfly6002', '百特妃兰', '6002-C04', 299.00, 1, 1, 4, 7, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (51, 0, '2024-05-05 23:04:57.232081', 0, '2024-05-05 23:04:57.232081', 0, 'powell61159', '伯韦尔', '61159-C22S', 299.00, 1, 1, 1, 7, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (52, 0, '2024-05-05 23:06:44.900821', 0, '2024-05-05 23:06:44.900821', 0, 'shanghaikiss-S5399', '情定上海', 'S5399-C1', 299.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (53, 0, '2024-05-05 23:08:10.088126', 0, '2024-05-05 23:08:10.088126', 0, 'butterfly8009', '百特妃兰', '8009-C06M', 299.00, 1, 1, 4, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (54, 0, '2024-05-05 23:10:35.180129', 0, '2024-05-05 23:10:35.180129', 0, 'powell62172', '伯韦尔', '62172-C2S', 299.00, 1, 1, 4, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (55, 0, '2024-05-05 23:12:03.456508', 0, '2024-05-05 23:12:03.456508', 0, 'wlc60004', '吴良材', '60004-C5', 299.00, 1, 1, 2, 3, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (56, 0, '2024-05-05 23:13:32.404368', 0, '2024-05-05 23:13:32.404368', 0, 'butterfly8014', '百特妃兰', '8014-C08', 299.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (57, 0, '2024-05-05 23:15:09.676547', 0, '2024-05-05 23:15:09.676547', 0, 'wlc60014', '吴良材', '60014-C6', 299.00, 1, 1, 1, 1, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (58, 0, '2024-05-05 23:17:38.454631', 0, '2024-05-05 23:17:38.455639', 0, 'wlc60017', '吴良材', '60017-C9', 199.00, 1, 1, 1, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (59, 0, '2024-05-05 23:19:23.927456', 0, '2024-05-05 23:19:23.927456', 0, 'wlc62158', '吴良材', '62158-C12S', 199.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (60, 0, '2024-05-05 23:21:18.104000', 0, '2024-05-05 23:21:18.104000', 0, 'shanghaikiss-SDFC9005', '情定上海', 'SDFC9005-C02', 199.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (61, 0, '2024-05-05 23:23:05.783145', 0, '2024-05-05 23:23:05.783145', 0, 'butterfly3126', '百特妃兰', '3126-C01', 199.00, 1, 1, 4, 7, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (62, 0, '2024-05-05 23:24:38.756518', 0, '2024-05-05 23:24:38.756518', 0, 'wlc5010', '吴良材', '5010-C7S', 199.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (63, 0, '2024-05-05 23:26:46.135503', 0, '2024-05-05 23:26:46.135503', 0, 'wlc62172', '吴良材', '62172-C8S', 199.00, 1, 1, 4, 5, 4);
INSERT INTO `maochang_eyeglassframeentry` VALUES (64, 0, '2024-05-05 23:28:23.045145', 0, '2024-05-05 23:28:23.045145', 0, 'shanghaikiss-SDFC9007', '情定上海', 'SDFC9007-C1', 199.00, 1, 1, 4, 5, 4);

-- ----------------------------
-- Table structure for maochang_eyeglassframeentrystyle
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframeentrystyle`;
CREATE TABLE `maochang_eyeglassframeentrystyle`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `entry_id` int NOT NULL,
  `style_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `maochang_eyeglassfra_entry_id_aed3827e_fk_maochang_`(`entry_id` ASC) USING BTREE,
  INDEX `maochang_eyeglassfra_style_id_345b240a_fk_maochang_`(`style_id` ASC) USING BTREE,
  CONSTRAINT `maochang_eyeglassfra_entry_id_aed3827e_fk_maochang_` FOREIGN KEY (`entry_id`) REFERENCES `maochang_eyeglassframeentry` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `maochang_eyeglassfra_style_id_345b240a_fk_maochang_` FOREIGN KEY (`style_id`) REFERENCES `maochang_eyeglassframestyletype` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 77 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframeentrystyle
-- ----------------------------
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (32, 0, '2024-05-05 20:50:58.622128', 0, '2024-05-05 20:50:58.623127', 0, 20, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (33, 0, '2024-05-05 20:55:57.201105', 0, '2024-05-05 20:55:57.201105', 0, 21, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (34, 0, '2024-05-05 21:05:23.390161', 0, '2024-05-05 21:05:23.390161', 0, 22, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (35, 0, '2024-05-05 21:09:59.443140', 0, '2024-05-05 21:09:59.443140', 0, 23, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (36, 0, '2024-05-05 21:16:18.879787', 0, '2024-05-05 21:16:18.879787', 0, 24, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (37, 0, '2024-05-05 21:19:45.145370', 0, '2024-05-05 21:19:45.145370', 0, 25, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (38, 0, '2024-05-05 21:25:25.681293', 0, '2024-05-05 21:25:25.681293', 0, 26, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (39, 0, '2024-05-05 21:31:56.089428', 0, '2024-05-05 21:31:56.089428', 0, 27, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (40, 0, '2024-05-05 21:38:13.006055', 0, '2024-05-05 21:38:13.006055', 0, 28, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (41, 0, '2024-05-05 21:43:00.697660', 0, '2024-05-05 21:43:00.697660', 0, 29, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (42, 0, '2024-05-05 21:46:08.284109', 0, '2024-05-05 21:46:08.284109', 0, 30, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (43, 0, '2024-05-05 21:50:13.718580', 0, '2024-05-05 21:50:13.718580', 0, 31, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (44, 0, '2024-05-05 21:53:26.337546', 0, '2024-05-05 21:53:26.337546', 0, 32, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (45, 0, '2024-05-05 21:57:32.673728', 0, '2024-05-05 21:57:32.674729', 0, 33, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (46, 0, '2024-05-05 22:07:48.722208', 0, '2024-05-05 22:07:48.722208', 0, 34, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (47, 0, '2024-05-05 22:13:01.814511', 0, '2024-05-05 22:13:01.814511', 0, 35, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (48, 0, '2024-05-05 22:16:05.728678', 0, '2024-05-05 22:16:05.728678', 0, 36, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (49, 0, '2024-05-05 22:20:54.473063', 0, '2024-05-05 22:20:54.473063', 0, 37, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (50, 0, '2024-05-05 22:24:05.070493', 0, '2024-05-05 22:24:05.070493', 0, 38, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (51, 0, '2024-05-05 22:27:07.144452', 0, '2024-05-05 22:27:07.144452', 0, 39, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (52, 0, '2024-05-05 22:30:15.449174', 0, '2024-05-05 22:30:15.449174', 0, 40, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (53, 0, '2024-05-05 22:37:56.146432', 0, '2024-05-05 22:37:56.146432', 0, 41, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (54, 0, '2024-05-05 22:40:02.149671', 0, '2024-05-05 22:40:02.149671', 0, 42, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (55, 0, '2024-05-05 22:42:04.074911', 0, '2024-05-05 22:42:04.074911', 0, 43, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (56, 0, '2024-05-05 22:44:27.581208', 0, '2024-05-05 22:44:27.581208', 0, 44, 4);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (57, 0, '2024-05-05 22:47:21.361215', 0, '2024-05-05 22:47:21.361215', 0, 45, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (58, 0, '2024-05-05 22:54:01.895186', 0, '2024-05-05 22:54:01.895186', 0, 46, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (59, 0, '2024-05-05 22:55:53.534206', 0, '2024-05-05 22:55:53.534206', 0, 47, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (60, 0, '2024-05-05 22:59:41.116529', 0, '2024-05-05 22:59:41.116529', 0, 48, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (61, 0, '2024-05-05 23:01:20.781562', 0, '2024-05-05 23:01:20.781562', 0, 49, 2);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (62, 0, '2024-05-05 23:03:23.008460', 0, '2024-05-05 23:03:23.008460', 0, 50, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (63, 0, '2024-05-05 23:04:57.298917', 0, '2024-05-05 23:04:57.298917', 0, 51, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (64, 0, '2024-05-05 23:06:45.001443', 0, '2024-05-05 23:06:45.001443', 0, 52, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (65, 0, '2024-05-05 23:08:10.166104', 0, '2024-05-05 23:08:10.166104', 0, 53, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (66, 0, '2024-05-05 23:10:35.293237', 0, '2024-05-05 23:10:35.293237', 0, 54, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (67, 0, '2024-05-05 23:12:03.531804', 0, '2024-05-05 23:12:03.531804', 0, 55, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (68, 0, '2024-05-05 23:13:32.477178', 0, '2024-05-05 23:13:32.477178', 0, 56, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (69, 0, '2024-05-05 23:15:09.749855', 0, '2024-05-05 23:15:09.749855', 0, 57, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (70, 0, '2024-05-05 23:17:38.559644', 0, '2024-05-05 23:17:38.559644', 0, 58, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (71, 0, '2024-05-05 23:19:23.995892', 0, '2024-05-05 23:19:23.995892', 0, 59, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (72, 0, '2024-05-05 23:21:18.228351', 0, '2024-05-05 23:21:18.228351', 0, 60, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (73, 0, '2024-05-05 23:23:05.904864', 0, '2024-05-05 23:23:05.904864', 0, 61, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (74, 0, '2024-05-05 23:24:38.827695', 0, '2024-05-05 23:24:38.827695', 0, 62, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (75, 0, '2024-05-05 23:26:46.207021', 0, '2024-05-05 23:26:46.207021', 0, 63, 1);
INSERT INTO `maochang_eyeglassframeentrystyle` VALUES (76, 0, '2024-05-05 23:28:23.115637', 0, '2024-05-05 23:28:23.115637', 0, 64, 1);

-- ----------------------------
-- Table structure for maochang_eyeglassframematerialtype
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframematerialtype`;
CREATE TABLE `maochang_eyeglassframematerialtype`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `material` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `material`(`material` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframematerialtype
-- ----------------------------
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (1, 0, '2024-04-30 04:30:47.659095', 0, '2024-04-30 04:30:47.659095', 0, '天然材料');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (2, 0, '2024-04-30 04:30:52.483000', 0, '2024-04-30 04:30:52.483000', 0, '贵金属');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (3, 0, '2024-04-30 04:30:58.011251', 0, '2024-04-30 04:30:58.011251', 0, '板材');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (4, 0, '2024-04-30 04:31:02.867413', 0, '2024-04-30 04:31:02.867413', 0, '钢材');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (5, 0, '2024-04-30 04:31:08.241282', 0, '2024-04-30 04:31:08.241282', 0, '钛材');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (6, 0, '2024-04-30 04:31:13.121561', 0, '2024-04-30 04:31:13.121561', 0, '合金');
INSERT INTO `maochang_eyeglassframematerialtype` VALUES (7, 0, '2024-04-30 04:31:17.910550', 0, '2024-04-30 04:31:17.910550', 0, '其他材料');

-- ----------------------------
-- Table structure for maochang_eyeglassframerecommendationrequest
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframerecommendationrequest`;
CREATE TABLE `maochang_eyeglassframerecommendationrequest`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `facial_width` decimal(15, 4) NOT NULL,
  `nose_width` decimal(15, 4) NOT NULL,
  `left_ear_distance` decimal(15, 4) NOT NULL,
  `right_ear_distance` decimal(15, 4) NOT NULL,
  `iris_center_distance` decimal(15, 4) NOT NULL,
  `left_eye_width` decimal(15, 4) NOT NULL,
  `right_eye_width` decimal(15, 4) NOT NULL,
  `left_eye_height` decimal(15, 4) NOT NULL,
  `right_eye_height` decimal(15, 4) NOT NULL,
  `inner_eyecorner_distance` decimal(15, 4) NOT NULL,
  `outter_eyecorner_distance` decimal(15, 4) NOT NULL,
  `face_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `skin_color` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `pupil_distance` decimal(15, 4) NOT NULL,
  `myopia_left` bigint NOT NULL,
  `myopia_right` bigint NOT NULL,
  `astigmatism_left` bigint NOT NULL,
  `astigmatism_right` bigint NOT NULL,
  `lens_weight` decimal(15, 4) NOT NULL,
  `gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` smallint NOT NULL,
  `career` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price_max` bigint NOT NULL,
  `price_min` bigint NOT NULL,
  `style_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `brand_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `material_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframerecommendationrequest
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_eyeglassframeshapetype
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframeshapetype`;
CREATE TABLE `maochang_eyeglassframeshapetype`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `shape` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `shape`(`shape` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframeshapetype
-- ----------------------------
INSERT INTO `maochang_eyeglassframeshapetype` VALUES (1, 0, '2024-04-30 04:35:29.488918', 0, '2024-04-30 04:35:29.488918', 0, '飞行员系列');
INSERT INTO `maochang_eyeglassframeshapetype` VALUES (2, 0, '2024-04-30 04:35:48.031703', 0, '2024-04-30 04:35:48.031703', 0, '异形');
INSERT INTO `maochang_eyeglassframeshapetype` VALUES (3, 0, '2024-04-30 04:36:03.174631', 0, '2024-04-30 04:36:03.174631', 0, '圆形或不规则圆形');
INSERT INTO `maochang_eyeglassframeshapetype` VALUES (4, 0, '2024-04-30 04:36:07.604459', 0, '2024-04-30 04:36:07.604459', 0, '方形或不规则方形');

-- ----------------------------
-- Table structure for maochang_eyeglassframestyletype
-- ----------------------------
DROP TABLE IF EXISTS `maochang_eyeglassframestyletype`;
CREATE TABLE `maochang_eyeglassframestyletype`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `style` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `style`(`style` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_eyeglassframestyletype
-- ----------------------------
INSERT INTO `maochang_eyeglassframestyletype` VALUES (1, 0, '2024-04-30 04:32:43.307003', 0, '2024-04-30 04:32:43.307003', 0, '复古经典风');
INSERT INTO `maochang_eyeglassframestyletype` VALUES (2, 0, '2024-04-30 04:32:47.895589', 0, '2024-04-30 04:32:47.895589', 0, '简约时尚风');
INSERT INTO `maochang_eyeglassframestyletype` VALUES (3, 0, '2024-04-30 04:32:52.477150', 0, '2024-04-30 04:32:52.477150', 0, '运动休闲风');
INSERT INTO `maochang_eyeglassframestyletype` VALUES (4, 0, '2024-04-30 04:32:58.891171', 0, '2024-04-30 04:32:58.891171', 0, '奢华个性风');

-- ----------------------------
-- Table structure for maochang_recommendationuser
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuser`;
CREATE TABLE `maochang_recommendationuser`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuser
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_recommendationuserbaseinfo
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuserbaseinfo`;
CREATE TABLE `maochang_recommendationuserbaseinfo`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `gender` smallint NOT NULL,
  `age_range` smallint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `maochang_recommendat_user_id_80a86d5b_fk_maochang_` FOREIGN KEY (`user_id`) REFERENCES `maochang_recommendationuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuserbaseinfo
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_recommendationuserfacialimage
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuserfacialimage`;
CREATE TABLE `maochang_recommendationuserfacialimage`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `frontview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `leftview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rightview` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `maochang_recommendat_user_id_e303af19_fk_maochang_` FOREIGN KEY (`user_id`) REFERENCES `maochang_recommendationuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuserfacialimage
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_recommendationuserfacialscanresult
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuserfacialscanresult`;
CREATE TABLE `maochang_recommendationuserfacialscanresult`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `outer_canthic_diameter` decimal(15, 4) NOT NULL,
  `inner_canthic_diameter` decimal(15, 4) NOT NULL,
  `eye_width_left` decimal(15, 4) NOT NULL,
  `eye_width_right` decimal(15, 4) NOT NULL,
  `eye_height_left` decimal(15, 4) NOT NULL,
  `eye_height_right` decimal(15, 4) NOT NULL,
  `ala_nasi_width` decimal(15, 4) NOT NULL,
  `nasion_width` decimal(15, 4) NOT NULL,
  `nose_height` decimal(15, 4) NOT NULL,
  `nose_pivot_angle` decimal(15, 4) NOT NULL,
  `head_width` decimal(15, 4) NOT NULL,
  `side_face_length_left` decimal(15, 4) NOT NULL,
  `side_face_length_right` decimal(15, 4) NOT NULL,
  `outer_canthic_ear_left` decimal(15, 4) NOT NULL,
  `outer_canthic_ear_right` decimal(15, 4) NOT NULL,
  `eyebrow_center_width` decimal(15, 4) NOT NULL,
  `face_height` decimal(15, 4) NOT NULL,
  `lip_width` decimal(15, 4) NOT NULL,
  `lip_height` decimal(15, 4) NOT NULL,
  `face_type` smallint NOT NULL,
  `skin_color_type` smallint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `maochang_recommendat_user_id_9f373143_fk_maochang_` FOREIGN KEY (`user_id`) REFERENCES `maochang_recommendationuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuserfacialscanresult
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_recommendationuserlens
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuserlens`;
CREATE TABLE `maochang_recommendationuserlens`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `refractive_index` decimal(15, 4) NOT NULL,
  `diameter` decimal(15, 4) NOT NULL,
  `density` decimal(15, 4) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `maochang_recommendat_user_id_ef71a64d_fk_maochang_` FOREIGN KEY (`user_id`) REFERENCES `maochang_recommendationuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuserlens
-- ----------------------------

-- ----------------------------
-- Table structure for maochang_recommendationuseroptometry
-- ----------------------------
DROP TABLE IF EXISTS `maochang_recommendationuseroptometry`;
CREATE TABLE `maochang_recommendationuseroptometry`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_user` int NOT NULL,
  `create_time` datetime(6) NULL DEFAULT NULL,
  `update_user` int NOT NULL,
  `update_time` datetime(6) NULL DEFAULT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `pupil_distance` decimal(15, 4) NOT NULL,
  `myopia_hyperopia_left` decimal(15, 4) NOT NULL,
  `myopia_hyperopia_right` decimal(15, 4) NOT NULL,
  `astigmatism_left` decimal(15, 4) NOT NULL,
  `astigmatism_right` decimal(15, 4) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `maochang_recommendat_user_id_0d3544ee_fk_maochang_` FOREIGN KEY (`user_id`) REFERENCES `maochang_recommendationuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of maochang_recommendationuseroptometry
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
