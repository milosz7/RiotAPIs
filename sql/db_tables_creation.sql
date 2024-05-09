# Jeremi Torój - 8/05/2024

CREATE DATABASE IF NOT EXISTS riot_api_data;
USE riot_api_data;

CREATE TABLE IF NOT EXISTS match_data (
    match_id varchar(15) NOT NULL,
    game_duration int NOT NULL,
    win varchar(4) NOT NULL,
    first_drake varchar(4) NOT NULL,
    dragon_kills tinyint NOT NULL,
    first_baron varchar(4) NOT NULL,
    surrender varchar(4) NOT NULL,
  PRIMARY KEY (`match_id`)
);

CREATE TABLE IF NOT EXISTS player_data (
    id int NOT NULL AUTO_INCREMENT,
    match_id varchar(15) NOT NULL,
    team_id varchar(4) NOT NULL,
    lane varchar(4) NOT NULL,
    'rank' varchar(10) NOT NULL,
    division tinyint NOT NULL,
    champion_name varchar(20) NOT NULL,
    first_blood tinyint NOT NULL,
    kills int NOT NULL,
    deaths int NOT NULL,
    assists int NOT NULL,
    dmg_per_min int NOT NULL,
    dmg_taken_per_min int NOT NULL,
    total_time_dead int NOT NULL,
    gold_per_min int NOT NULL,
    wards_placed int NOT NULL,
    sight_wards_bought int NOT NULL,
    wards_destroyed int NOT NULL,
    vision_score_per_minute int NOT NULL,
    dmg_to_towers int NOT NULL,
    cs_per_minute int NOT NULL,
    missing_pings int NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS champion_bans (
    match_id varchar(15) NOT NULL,
    ban_1 int NOT NULL,
    ban_2 int NOT NULL,
    ban_3 int NOT NULL,
    ban_4 int NOT NULL,
    ban_5 int NOT NULL,
    ban_6 int NOT NULL,
    ban_7 int NOT NULL,
    ban_8 int NOT NULL,
    ban_9 int NOT NULL,
    ban_10 int NOT NULL,
    PRIMARY KEY (`match_id`)
);

CREATE TABLE IF NOT EXISTS champions (
    champion_id int NOT NULL,
    champion_name varchar(20) NOT NULL,
    PRIMARY KEY (`champion_id`)
);
