SET FOREIGN_KEY_CHECKS=0;


-- ----------------------------
-- Table structure for tencent
-- ----------------------------
DROP TABLE IF EXISTS `singer`;
CREATE TABLE `singer` (
  `name` varchar(128) NOT NULL,
  `id` varchar(64) NOT NULL,
  `type` varchar(64) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;


