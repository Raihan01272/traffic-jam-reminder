import sqlite3

connection = sqlite3.connect("traffic_jam.db")
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