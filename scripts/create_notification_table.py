import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "traffic_jam.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_link TEXT NOT NULL UNIQUE,
        article_tittle TEXT NOT NULL,
        sent_at TEXT DEFAULT (datetime('now'))
    )
""")

connection.commit()

print("Tabel notification_history berhasil dibuat!")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name = 'notification_history'
""")

print("Hasil pemeriksaan:", cursor.fetchone())

connection.close()