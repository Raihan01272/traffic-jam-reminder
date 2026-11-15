import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "traffic_jam.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    ALTER TABLE notification_history
    RENAME COLUMN article_tittle TO article_title
""")

connection.commit()

print("Nama kolom berhasil diperbaiki!")

cursor.execute("PRAGMA table_info(notification_history)")

for column in cursor.fetchall():
    print(column)

connection.close()