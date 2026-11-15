import sqlite3

def is_article_sent(article_link):
    connection = sqlite3.connect("traffic_jam.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 1
        FROM notification_history
        WHERE article_link = ?
    """, (article_link,))

    result = cursor.fetchone()
    connection.close()

    return result is not None

def save_sent_article(article_link, article_title):
    connection = sqlite3.connect("traffic_jam.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO notification_history (
            article_link,
            article_title
        )
        VALUES (?, ?)
    """, (article_link, article_title))

    connection.commit()

    if cursor.rowcount == 1:
        print("Berita berhasil dicatat!")
    else:
        print("Berita sudah tercata sebelumnya.")

    connection.close()

if __name__ == "__main__":

    sample_link = "https://example.com/dummy/tawuran-priok"
    sample_title = "Tawuran Terjadi di Tanjung Priok"

    if is_article_sent(sample_link):
         print("Berita sudah pernah dikirim.")
    else:
        print("Berita belum pernah dikirim.")

        save_sent_article(sample_link, sample_title)

    if is_article_sent(sample_link):
        print("Verifikasi: berita sekarang sudah tercatat.")
    else:
        print("Verifikasi: berita belum tercatat.")