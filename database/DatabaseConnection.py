from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
import os


class DatabaseConnection:
    def __init__(self, dotenv_path: str, timeout: int = 10):
        load_dotenv(dotenv_path=dotenv_path)
        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=DictCursor,
            db=os.getenv('DB'),
            host=os.getenv('HOST'),
            password=os.getenv('PASS'),
            read_timeout=timeout,
            port=int(os.getenv('PORT')),
            user=os.getenv('USER'),
            write_timeout=timeout,
        )

    def __del__(self):
        self.connection.close()

    def query(self, query: str, args: tuple = ()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchall()

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

    def add_champion_bans(self, match_id: int, ban_1: int, ban_2: int, ban_3: int, ban_4: int, ban_5: int, ban_6: int,
                          ban_7: int, ban_8: int, ban_9: int, ban_10: int):
        self.query("INSERT INTO champion_bans (match_id, ban_1, ban_2, ban_3, ban_4, ban_5,"
                   " ban_6, ban_7, ban_8, ban_9, ban_10)"
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (match_id, ban_1, ban_2, ban_3, ban_4, ban_5, ban_6, ban_7, ban_8, ban_9, ban_10))
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
