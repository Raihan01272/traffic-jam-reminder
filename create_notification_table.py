import sqlite3

connection = sqlite3.connect("traffic_jam.db")
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