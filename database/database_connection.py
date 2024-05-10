import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path

timeout = 10
#insert your own path to .env file
dotenv_path = Path('../../../Desktop/.env')
load_dotenv(dotenv_path=dotenv_path)

connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=os.getenv('DB'),
    host=os.getenv('HOST'),
    password=os.getenv('PASS'),
    read_timeout=timeout,
    port=11092,
    user="avnadmin",
    write_timeout=timeout,
)

database_creation = """CREATE DATABASE IF NOT EXISTS defaultdb;"""

match_data_table = """CREATE TABLE IF NOT EXISTS match_data (
    match_id varchar(15) NOT NULL,
    game_duration int NOT NULL,
    win varchar(4) NOT NULL,
    first_drake varchar(4) NOT NULL,
    dragon_kills tinyint NOT NULL,
    first_baron varchar(4) NOT NULL,
    surrender varchar(4) NOT NULL,
    CONSTRAINT PK_match_id PRIMARY KEY (`match_id`)
);
"""

champions_table = """CREATE TABLE IF NOT EXISTS champions (
    champion_id int NOT NULL,
    champion_name varchar(20) NOT NULL,
    CONSTRAINT PK_champion_id PRIMARY KEY (`champion_id`)
);"""

player_data_table = """CREATE TABLE IF NOT EXISTS player_data (
    id int NOT NULL AUTO_INCREMENT,
    match_id varchar(15) NOT NULL,
    team_id varchar(4) NOT NULL,
    lane varchar(4) NOT NULL,
    `rank` varchar(10) NOT NULL,
    division tinyint NOT NULL,
    champion_id int NOT NULL,
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
    CONSTRAINT PK_id PRIMARY KEY (`id`),
    CONSTRAINT FK_player_data_match FOREIGN KEY (match_id) REFERENCES match_data(match_id),
    CONSTRAINT FK_player_data_champion FOREIGN KEY (champion_id) REFERENCES champions(champion_id)
);"""

champion_bans_table = """CREATE TABLE IF NOT EXISTS champion_bans (
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
    CONSTRAINT PK_champion_bans PRIMARY KEY (`match_id`),
    CONSTRAINT FK_champion_bans_match FOREIGN KEY (match_id) REFERENCES match_data(match_id)
);"""

test_insert = "INSERT INTO champions (champion_id, champion_name) VALUES (266, 'Aatrox')"
test = "SELECT * FROM champions"

try:
    cursor = connection.cursor()

    #print(cursor.execute(test_insert))
    #always
    connection.commit()
    print(cursor.execute(test))
    print(cursor.fetchall())


finally:
    connection.close()