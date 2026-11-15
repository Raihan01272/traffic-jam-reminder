import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "traffic_jam.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    SELECT article_title, article_link, sent_at
    FROM notification_history
    ORDER BY id DESC
""")

rows = cursor.fetchall()

print("\n=== RIWAYAT NOTIFIKASI ===")

for row in rows:
    print("Title:", row[0])
    print("Link:", row[1])
    print("Sent At:", row[2])
    print("-" * 50)

print("Total Notifikasi:", len(rows))

connection.close()