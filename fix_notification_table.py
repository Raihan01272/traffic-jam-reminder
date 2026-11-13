import sqlite3

connection = sqlite3.connect("traffic_jam.db")
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