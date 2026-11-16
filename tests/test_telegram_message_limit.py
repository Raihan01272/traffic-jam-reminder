
from notifications.telegram_notifier import send_telegram_notifications


test_articles = []

for i in range(1, 31):

    article = {
        "source": "Detik.com",
        "title": f"Simulasi laporan gangguan lalu lintas Tanjung Priok nomor {i}",
        "link": f"https://example.com/test-{i}",
        "incident_category": "KECELAKAAN_DAN_MACET",
        "location_category": "MAIN",
        "published_at": None
    }

    test_articles.append(article)


send_telegram_notifications(
    test_articles,
    all_sources_success=True,
    dry_run=True
)