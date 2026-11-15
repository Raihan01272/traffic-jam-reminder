import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "traffic_jam.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("=== PEMERIKSAAN UNIQUE INDEX ===")

cursor.execute("PRAGMA index_list(news_articles)")
indexes = cursor.fetchall()

print("Daftar index:", indexes)

for index in indexes:
    index_name = index[1]

    cursor.execute(f"PRAGMA index_info('{index_name}')")
    columns = cursor.fetchall()

    print("Nama index:", index_name)
    print("Kolom:", columns)

connection.close()