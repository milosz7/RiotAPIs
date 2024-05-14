from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
import os


class DatabaseConnection:
    def __init__(self, dotenv_path: str, timeout: int = 10):
        load_dotenv(dotenv_path=dotenv_path)
        envs = ['DB', 'HOST', 'PASS', 'PORT', 'USER']
        for env in envs:
            if not os.environ.get(env):
                raise ValueError(f"Missing environment variable {env} in .env file.")

        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=DictCursor,
            db=os.getenv('DB'),
            host=os.getenv('HOST'),
            password=os.getenv('PASS'),
            read_timeout=timeout,
            port=int(os.getenv('PORT')),
            user=os.getenv('DB_USER'),
            write_timeout=timeout,
        )

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

    def query(self, query: str, args: tuple = ()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchall()

    @staticmethod
    def generate_add_query(table: str, columns: list, values: list):
        return f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join((str(v) for v in values))})"

    def generate_update_query(self):
        raise NotImplementedError

    def get_champions(self):
        return self.query("SELECT * FROM champions")

    def add_champion(self, champ_id: int, name: str):
        self.query("INSERT INTO champions (champion_id, champion_name) VALUES (%s, %s)", (champ_id, name))
        self.connection.commit()

    def delete_champion(self, champ_id: int):
        self.query("DELETE FROM champions WHERE champion_id = %s", (champ_id,))
        self.connection.commit()

    def update_champion(self, champ_id: int, name: str):
        self.query("UPDATE champions SET champion_name = %s WHERE champion_id = %s", (name, champ_id))
        self.connection.commit()

    def get_champion_bans(self):
        return self.query("SELECT * FROM champion_bans")

    def add_champion_bans(self, match_id: str, bans: list):
        ban_columns = ["match_id"] + [f"ban_{i}" for i in range(1, 11)]
        ban_values = [match_id] + bans

        sql = self.generate_add_query("champion_bans", ban_columns, ban_values)
        self.query(sql)
        self.connection.commit()

    def delete_champion_bans(self, match_id: int):
        self.query("DELETE FROM champion_bans WHERE match_id = %s", (match_id,))
        self.connection.commit()

    def update_champion_bans(self, match_id: int, ban_1: int, ban_2: int, ban_3: int, ban_4: int, ban_5: int,
                             ban_6: int, ban_7: int, ban_8: int, ban_9: int, ban_10: int):
        self.query("UPDATE champion_bans SET ban_1 = %s, ban_2 = %s, ban_3 = %s, ban_4 = %s, ban_5 = %s,"
                   " ban_6 = %s, ban_7 = %s, ban_8 = %s, ban_9 = %s, ban_10 = %s WHERE match_id = %s",
                   (ban_1, ban_2, ban_3, ban_4, ban_5, ban_6, ban_7, ban_8, ban_9, ban_10, match_id))
        self.connection.commit()

    def get_matches(self):
        return self.query("SELECT * FROM match_data")

    def add_match(self, match_id: int, game_duration: int, win: str, first_drake: str, dragon_kills: int,
                  first_baron: str, surrender: int):
        self.query("INSERT INTO match_data (match_id, game_duration, win,"
                   " first_drake, dragon_kills, first_baron, surrender)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (match_id, game_duration, win, first_drake, dragon_kills, first_baron, surrender))
        self.connection.commit()

    def delete_match(self, match_id: int):
        self.query("DELETE FROM match_data WHERE match_id = %s", (match_id,))
        self.connection.commit()

    def update_match(self, match_id: int, game_duration: int, win: str, first_drake: str, dragon_kills: int,
                     first_baron: str, surrender: str):
        self.query("UPDATE match_data SET game_duration = %s, win = %s, first_drake = %s, dragon_kills = %s,"
                   " first_baron = %s, surrender = %s WHERE match_id = %s",
                   (game_duration, win, first_drake, dragon_kills, first_baron, surrender, match_id))
        self.connection.commit()

    def get_player_data(self):
        return self.query("SELECT * FROM player_data")

    def add_player_data(self, match_id: int, team_id: int, lane: str, rank: str, division: int, champion_id: int,
                        first_blood: int, kills: int, deaths: int, assists: int, dmg_per_min: int,
                        dmg_taken_per_min: int, total_time_dead: int, gold_per_min: int, wards_placed: int,
                        sight_wards_bought: int, wards_destroyed: int, vision_score_per_min: int, dmg_to_towers: int,
                        cs_per_min: int, missing_pings: int):
        self.query("INSERT INTO player_data (match_id, team_id, lane, `rank`, division, champion_id,"
                   " first_blood, kills, deaths, assists, dmg_per_min, dmg_taken_per_min, total_time_dead,"
                   " gold_per_min, wards_placed, sight_wards_bought, wards_destroyed, vision_score_per_min,"
                   " dmg_to_towers, cs_per_min, missing_pings)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (match_id, team_id, lane, rank, division, champion_id, first_blood, kills, deaths,
                    assists, dmg_per_min, dmg_taken_per_min, total_time_dead, gold_per_min, wards_placed,
                    sight_wards_bought, wards_destroyed, vision_score_per_min, dmg_to_towers, cs_per_min,
                    missing_pings))
        self.connection.commit()

    def delete_player_data(self, match_id: int):
        self.query("DELETE FROM player_data WHERE match_id = %s", (match_id,))
        self.connection.commit()

    def update_player_data(self, match_id: int, team_id: int, lane: str, rank: str, division: int, champion_id: int,
                           first_blood: int, kills: int, deaths: int, assists: int, dmg_per_min: int,
                           dmg_taken_per_min: int, total_time_dead: int, gold_per_min: int, wards_placed: int,
                           sight_wards_bought: int, wards_destroyed: int, vision_score_per_min: int, dmg_to_towers: int,
                           cs_per_min: int, missing_pings: int):

        self.query("UPDATE player_data SET team_id = %s, lane = %s, `rank` = %s, division = %s, champion_id = %s,"
                   " first_blood = %s, kills = %s, deaths = %s, assists = %s, dmg_per_min = %s,"
                   " dmg_taken_per_min = %s, total_time_dead = %s, gold_per_min = %s, wards_placed = %s,"
                   " sight_wards_bought = %s, wards_destroyed = %s, vision_score_per_min = %s,"
                   " dmg_to_towers = %s, cs_per_min = %s, missing_pings = %s WHERE match_id = %s",
                   (team_id, lane, rank, division, champion_id, first_blood, kills, deaths, assists, dmg_per_min,
                    dmg_taken_per_min, total_time_dead, gold_per_min, wards_placed, sight_wards_bought, wards_destroyed,
                    vision_score_per_min, dmg_to_towers, cs_per_min, missing_pings, match_id))
        self.connection.commit()
