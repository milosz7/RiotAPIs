from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
import os


class DatabaseConnection:
    def __init__(self, dotenv_path: str, timeout: int=10):
        load_dotenv(dotenv_path=dotenv_path)
        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=DictCursor,
            db=os.getenv('DB'),
            host=os.getenv('HOST'),
            password=os.getenv('PASS'),
            read_timeout=timeout,
            port=11092,
            user="avnadmin",
            write_timeout=timeout,
        )
