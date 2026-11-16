
import sqlite3

connection = sqlite3.connect("traffic_jam.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT article_link, article_title
    FROM notification_history
    ORDER BY id DESC
    LIMIT 10
""")

rows = cursor.fetchall()

print("\n=== NOTIFICATION HISTORY ===")

for row in rows:
    print("Link:", row[0])
    print("Judul:", row[1])
    print("-" * 40)

connection.close()
