import os
import requests

from multi_source_scraper import alert_articles
from notification_manager import is_article_sent, save_sent_article

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if not bot_token or not chat_id:
    raise ValueError("Token atau Chat ID belum tersedia!")

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

new_alert_articles = []

for article in alert_articles:
    article_link = article["link"]

    if is_article_sent(article_link):
        print("Berita sudah pernah dikirim:", article["title"])
    else:
        new_alert_articles.append(article)

if new_alert_articles:

    message = "macet bang, cari alternatif lain jalannya biar ga telat ngantor"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    if result.get("ok"):
        for article in new_alert_articles:
            save_sent_article(
                article["link"],
                article["title"]
            )

        print("Pesan alert berhasil dikirim!")
        print("Total berita baru:", len(new_alert_articles))

    else:
        print("Pengiriman pesan gagal!")

elif len(alert_articles) == 0:

    message = "aman bang lancar kayaknya"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    response.raise_for_status()

    if response.json().get("ok"):
        print("Pesan kondisi aman berhasil dikirim!")

else:
    print("Tidak ada berita alert baru. Notifikasi tidak dikirim.")