import sqlite3

connection = sqlite3.connect("traffic_jam.db")
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM news_articles")
before = cursor.fetchone()[0]

print("Jumlah sebelum:", before)

for i in range(2):
    cursor.execute("""
        INSERT OR IGNORE INTO news_articles (
            source,
            title,
            description,
            link,
            location_category,
            incident_category,
            scraped_at
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        "Test Source",
        "Artikel Pengujian Duplikat",
        "Artikel untuk menguji pencegahan duplikasi.",
        "https://example.com/test-duplicate",
        "MAIN",
        "TAWURAN"
    ))

connection.commit()

cursor.execute("SELECT COUNT(*) FROM news_articles")
after = cursor.fetchone()[0]

print("Jumlah setelah:", after)
print("Artikel yang berhasil ditambahkan:", after - before)

connection.close()
