
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `news_yangxian`;
CREATE TABLE `news_yangxian` (
               `id` int(11) NOT NULL AUTO_INCREMENT,
               `title`  varchar(16128) NOT  NULL,
               `url`  varchar(128) DEFAULT NULL,
               `public_time`   datetime DEFAULT NULL,
               `auth`    varchar(16) DEFAULT NULL,
               `edit`    varchar(16) DEFAULT NULL,
               `content`  text DEFAULT NULL,
              PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT  CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;



SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `news_baliguan`;
CREATE TABLE `news_baliguan` (
               `id` int(11) NOT NULL AUTO_INCREMENT,
               `title`  varchar(16128) NOT  NULL,
               `url`  varchar(128) DEFAULT NULL,
               `public_time`   datetime DEFAULT NULL,
               `auth`    varchar(16) DEFAULT NULL,
               `edit`    varchar(16) DEFAULT NULL,
               `content`  text DEFAULT NULL,
              PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT  CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;




