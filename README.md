TimeTraktor
===========

Tracking my time in MySQL

# Installation

## MySQL
```sql
CREATE TABLE `timetracking` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` enum('karamfil') NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `window_class` varchar(200) NOT NULL,
  `window_title` varchar(200) NOT NULL,
  `time` smallint(4) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`,`date`,`time`,`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1554 DEFAULT CHARSET=utf8
```

## Flask
`pip install flask`

# Run
## Traktor
`python traktor.py`

## Viewer
`python viewer.py`