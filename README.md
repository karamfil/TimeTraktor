Time-Traker
===========

Tracking my time in MySQL

# Installation

## MySQL
```sql
CREATE TABLE `timetracking` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` enum('username') NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `window_class` varchar(250) NOT NULL,
  `window_title` varchar(250) NOT NULL,
  `time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```

## Flask
`pip install flask`

# Run
## Traktor
`python traktor.py`

## Viewer
`python viewer.py`