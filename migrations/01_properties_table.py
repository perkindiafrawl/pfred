CREATE TABLE IF NOT EXISTS `properties` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `is_sold` int(1) NOT NULL DEFAULT '0',
  `lat` float DEFAULT NULL,
  `long` float DEFAULT NULL,
  `address1` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `zip` varchar(255) DEFAULT NULL,
  `url` varchar(2000) DEFAULT NULL,
  `property_type` varchar(65) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `beds` varchar(255) DEFAULT NULL,
  `baths` varchar(255) DEFAULT NULL,
  `square_footage` float DEFAULT NULL,
  `source` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lat` (`lat`,`long`,`source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
