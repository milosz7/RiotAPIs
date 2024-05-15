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
            return cursor.execute(query, args)

    @staticmethod
    def generate_add_query(table: str, columns: list, values: list):
        values = (f"'{v}'" if isinstance(v, str) or v is None else str(v) for v in values)
        return f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)});"

    @staticmethod
    def generate_update_query(table: str, condition: tuple, columns: list, values: list):
        key_column, key_value = condition
        set_clause = ", ".join([f"{col} = {val}" for col, val in zip(columns, values)])
        return f"UPDATE {table} SET {set_clause} WHERE {key_column} = {key_value};"

    def get_champions(self):
        return self.query("SELECT * FROM champions")

    def add_champion(self, champ_id: int, name: str):
        columns = ["champion_id", "champion_name"]
        values = [champ_id, name]

        sql = self.generate_add_query("champions", columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def delete_champion(self, champ_id: int):
        rows_affected = self.query("DELETE FROM champions WHERE champion_id = %s", (champ_id,))
        self.connection.commit()

        return rows_affected

    def update_champion(self, champ_data: dict):
        condition = ("champion_id", champ_data.pop("champion_id"))
        columns = list(champ_data.keys())
        values = list(champ_data.values())

        sql = self.generate_update_query("champions", condition, columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def get_champion_bans(self):
        return self.query("SELECT * FROM champion_bans")

    def add_champion_bans(self, match_id: str, bans: list):
        ban_columns = ["match_id"] + [f"ban_{i}" for i in range(1, 11)]
        ban_values = [match_id] + bans

        sql = self.generate_add_query("champion_bans", ban_columns, ban_values)
        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def delete_champion_bans(self, match_id: int):
        rows_affected = self.query("DELETE FROM champion_bans WHERE match_id = %s", (match_id,))
        self.connection.commit()

        return rows_affected

    def update_champion_bans(self, ban_data: dict):
        condition = ("match_id", ban_data.pop("match_id"))

        columns = list(ban_data.keys())
        values = list(ban_data.values())

        sql = self.generate_update_query("champion_bans", condition, columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def get_matches(self):
        return self.query("SELECT * FROM match_data")

    def add_match(self, match_data: dict):
        columns = list(match_data.keys())
        values = list(match_data.values())
        sql = self.generate_add_query("match_data", columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def delete_match(self, match_id: int):
        rows_affected = self.query("DELETE FROM match_data WHERE match_id = %s", (match_id,))
        self.connection.commit()

        return rows_affected

    def update_match(self, match_data: dict):
        condition = ("match_id", match_data.pop("match_id"))

        columns = list(match_data.keys())
        values = list(match_data.values())

        sql = self.generate_update_query("match_data", condition, columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def get_player_data(self):
        return self.query("SELECT * FROM player_data")

    def add_player_data(self, player_data: dict):
        columns = list(player_data.keys())
        values = list(player_data.values())
        sql = self.generate_add_query("player_data", columns, values)
        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected

    def delete_player_data(self, match_id: int):
        rows_affected = self.query("DELETE FROM player_data WHERE match_id = %s", (match_id,))
        self.connection.commit()

        return rows_affected

    def update_player_data(self, player_data: dict):
        condition = ("id", player_data.pop("id"))

        columns = list(player_data.keys())
        values = list(player_data.values())

        sql = self.generate_update_query("player_data", condition, columns, values)

        rows_affected = self.query(sql)
        self.connection.commit()

        return rows_affected
