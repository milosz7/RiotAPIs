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

try:
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    print(cursor.fetchall())
finally:
    connection.close()