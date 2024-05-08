CREATE DATABASE IF NOT EXISTS 'riot_api_data' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `riot_api_data`;

CREATE TABLE IF NOT EXISTS `match_data` (
    match_id varchar(15) NOT NULL,
    game_duration int NOT NULL,
    win varchar(4) NOT NULL,
    first_drake varchar(4) NOT NULL,
    dragon_kills tinyint NOT NULL,
    first_baron varchar(4) NOT NULL,
    surrender varchar(4) NOT NULL,
  PRIMARY KEY (`match_id`)
) DEFAULT CHARSET=utf8;



