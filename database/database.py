import sqlite3


def save_articles(valid_articles):
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
            article.get("location_category", "NOT_RELEVANT"),
            article.get("incident_category", "NONE")
        ))

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM news_articles")
    total_articles = cursor.fetchone()[0]

    print("Total artikel di database:", total_articles)

    connection.close()

    return total_articles


def check_database_structure():
    connection = sqlite3.connect("traffic_jam.db")
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(news_articles)")
    columns = cursor.fetchall()

    print("\n=== DATABASE TABLE STRUCTURE ===")

    for column in columns:
        print(column)

    cursor.execute("PRAGMA index_list(news_articles)")
    indexes = cursor.fetchall()

    print("\n=== DATABASE INDEXES ===")

    for index in indexes:
        print(index)

    print("\n=== UNIQUE INDEX DETAILS ===")

    for index in indexes:
        index_name = index[1]

        cursor.execute(f"PRAGMA index_info('{index_name}')")
        index_columns = cursor.fetchall()

        print(f"\nIndex: {index_name}")

        for column in index_columns:
            print("Kolom UNIQUE:", column[2])

    connection.close()

def check_articles_by_source():
    connection = sqlite3.connect("traffic_jam.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT source, COUNT(*)
        FROM news_articles
        GROUP BY SOURCE
        ORDER BY SOURCE
    """)

    results = cursor.fetchall()

    print("\n=== ARTICLES BY SOURCE ===")

    for source, total in results:
        print(f"{source:<20}: {total}")

    connection.close()


if __name__ == "__main__":
    print("Database module berhasil dijalankan.")
    check_database_structure()
    check_articles_by_source()