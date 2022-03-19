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
(1,'admin@admin.com','admin','pbkdf2:sha256:260000$lLcpJVgwBDSGP393$cc497e2610c6a7cd2369bf06c26cac914ca3d0b36b5d348045f6f9baab3ae2a0');



CREATE TABLE `log` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`ip` varchar(20) NOT NULL,
`email` varchar(50) NOT NULL,
`boolcheck` tinyint(1),
`date` DATE,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `task` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` varchar(128) NOT NULL,
`name` varchar(128) NOT NULL,
`status` varchar(30) NOT NULL DEFAULT 'PENDING',
`starttime` varchar(30) NOT NULL,
`endtime` varchar(30) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `scanTask` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`pid` varchar(128) NOT NULL,
`tid` varchar(128) NOT NULL,
`url` varchar(128) NOT NULL,
`status` varchar(30) NOT NULL DEFAULT 'PENDING',
`starttime` varchar(30) NOT NULL,
`endtime` varchar(30) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `baseinfo` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` varchar(128) NOT NULL,
`url` varchar(50) NOT NULL,
`status` varchar(3) NOT NULL,
`title` varchar(50),
`date` varchar(30),
`responseheader` TEXT,
`Server` TEXT,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `VulList` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` varchar(128) NOT NULL,
`url` varchar(50) NOT NULL,
`pocname` varchar(128),
`result`  TEXT,
`created` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `PocList` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`status` tinyint(1) DEFAULT 0,
`position` tinyint(1) DEFAULT 0,
`filename` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `pluginList` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`status` tinyint(1) DEFAULT 0,
`position` tinyint(1) DEFAULT 0,
`filename` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `ExtList` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
`tid` varchar(128) NOT NULL,
`pluginname` varchar(128),
`result` TEXT,
`created` varchar(128) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





