import sqlite3

from multi_source_scraper import valid_articles

connection = sqlite3.connect("traffic_jam.db")
cursor = connection.cursor()

for article in valid_articles:
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
        article["source"],
        article["title"],
        article["description"],
        article["link"],
        article["location_category"],
        article["incident_category"]
    ))

connection.commit()

cursor.execute("SELECT COUNT(*) FROM news_articles")
total_articles = cursor.fetchone()[0]

print("Total artikel do database:", total_articles)

connection.close()