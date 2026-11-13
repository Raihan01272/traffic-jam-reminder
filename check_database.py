import sqlite3

connection = sqlite3.connect("traffic_jam.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT COUNT(*)
    FROM news_articles
""")

total_articles = cursor.fetchone()[0]

print("=== DATABASE SUMMARY ====")
print("Total Articles:", total_articles)

cursor.execute("""
    SELECT
        id,
        source,
        title,
        location_category,
        incident_category
    FROM news_articles
    ORDER BY id DESC
    LIMIT 5
""")

articles = cursor.fetchall()

print("\n=== LATEST 5 ARTICLES ===")

for article in articles:
    print("\nID:", article[0])
    print("Source:", article[1])
    print("Title:", article[2])
    print("Location:", article[3])
    print("Incident:", article[4])
    print("-" * 50)

cursor.execute("""
    SELECT source, COUNT(*)
    FROM news_articles
    GROUP BY source
""")

source_counts = cursor.fetchall()

print("\n=== ARTICLES BY SOURCE ===")

for source, total in source_counts:
    print(source, ":", total)

cursor.execute("""
    SELECT link, COUNT(*)
    FROM news_articles
    GROUP BY link
    HAVING COUNT(*) > 1
""")

duplicate_links = cursor.fetchall()

print("\n=== DUPLICATE URL CHECK ===")
print("Duplicate URLs:", len(duplicate_links))

cursor.execute("""
    SELECT COUNT(*)
    FROM news_articles
    WHERE source IS NULL OR source = ''
        OR title IS NULL OR title = ''
        OR link IS NULL OR link = ''
""")

invalid_count = cursor.fetchone()[0]

print("\n=== REQUIRED DATA CHECK ===")
print("Articles with missing required data:", invalid_count)

cursor.execute("""
    SELECT COUNT(*)
    FROM news_articles
    WHERE location_category IS NULL
        OR incident_category IS NULL
""")

missing_category = cursor.fetchone()[0]

print("\n=== CATEGORY CHECK ===")
print("Articles with missing categories:", missing_category)

connection.close()

print("\nDatabase inspection selesai!")