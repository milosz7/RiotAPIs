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

    def display_champions(self):
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
