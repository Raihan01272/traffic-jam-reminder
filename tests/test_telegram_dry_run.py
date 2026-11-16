from notifications.telegram_notifier import send_telegram_notifications


test_articles = [
    {
        "source": "Detik.com",
        "title": "Simulasi kemacetan di Jalan Yos Sudarso",
        "link": "https://example.com/test-1",
        "incident_category": "KECELAKAAN_DAN_MACET",
        "location_category": "MAIN",
        "published_at": None
    },
    {
        "source": "CNA Indonesia",
        "title": "Simulasi gangguan jalan di Tanjung Priok",
        "link": "https://example.com/test-2",
        "incident_category": "GANGGUAN_JALAN",
        "location_category": "MAIN",
        "published_at": None
    }
]


send_telegram_notifications(
    test_articles,
    all_sources_success=True,
    dry_run=True
)