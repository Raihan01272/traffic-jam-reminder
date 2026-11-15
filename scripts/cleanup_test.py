import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "traffic_jam.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    DELETE FROM news_articles
    WHERE link = ?
""", ("https://example.com/test-duplicate",))

connection.commit()

print("Artikel pengujian berhasil dihapus.")
print("Jumlah baris yang dihapus:", cursor.rowcount)

cursor.execute("SELECT COUNT(*) FROM news_articles")
total_articles = cursor.fetchone()[0]

print("Total artikel sekarang:", total_articles)

connection.close()