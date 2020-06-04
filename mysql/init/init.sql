CREATE DATABASE IF NOT EXISTS SZheScan default charset utf8 COLLATE utf8_general_ci;

use SZheScan;

CREATE TABLE `user` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`email` varchar(20) NOT NULL,
`username` varchar(50) NOT NULL,
`pw_hash` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (`id`, `email`, `username`, `pw_hash`)
VALUES
(1,'springbird@qq.com','springbird','pbkdf2:sha256:150000$XNEKW4J4$726b6b5f7d07c3e7f4280634b547b90c64055018f31290c05857aade0b983057');

CREATE TABLE `profile` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`userid` int(11) NOT NULL,
`blog` varchar(100) NULL,
`signature` TEXT NULL,

PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `baseinfo` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`url` varchar(50) NOT NULL,
`status` varchar(4) NOT NULL,
`title` varchar(50),
`date` varchar(30) NOT NULL,
`responseheader` TEXT NOT NULL,
`Server` TEXT,
`portserver` TEXT,
`sendir` TEXT,
`boolcheck` tinyint(1),
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `ipinfo` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`baseinfoid` int(11) NOT NULL,
`bindingdomain` TEXT,
`sitestation` TEXT,
`CMessage` TEXT NOT NULL,
`ipaddr` varchar(100) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `domaininfo` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`baseinfoid` int(11) NOT NULL,
`subdomain` TEXT,
`whois` TEXT,
`bindingip` TEXT,
`sitestation` TEXT,
`recordinfo` TEXT,
`domainaddr` varchar(200),
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `buglist` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`oldurl` varchar(50),
`bugurl` varchar(200),
`bugname` varchar(100) NOT NULL,
`buggrade` varchar(7) NOT NULL,
`payload` varchar(100),
`bugdetail` TEXT,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `poc` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`name` varchar(100) NOT NULL,
`rule` TEXT,
`expression` TEXT,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `log` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`ip` varchar(20) NOT NULL,
`email` varchar(50) NOT NULL,
`date` DATE,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `invitationcode` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`code` varchar(36) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



