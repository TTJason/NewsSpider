/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : news_dataset

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-07-30 11:51:01
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tencent
-- ----------------------------
DROP TABLE IF EXISTS `tencent`;
CREATE TABLE `tencent` (
  `title` varchar(128) NOT NULL,
  `content` varchar(20000) NOT NULL,
  `date` varchar(64) NOT NULL,
  `id` varchar(64) NOT NULL,
  `cname` varchar(64) NOT NULL,
  `url` varchar(128) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
