
from notifications.telegram_notifier import send_telegram_notifications


test_articles = [
    {
        "source": "Detik.com",
        "title": "Simulasi kemacetan di Jalan Yos Sudarso",
        "link": "https://example.com/test-failure",
        "incident_category": "KECELAKAAN_DAN_MACET",
        "location_category": "MAIN",
        "published_at": None
    }
]


send_telegram_notifications(
    test_articles,
    all_sources_success=False,
    dry_run=True,
    source_status={
        "Detik.com": True,
        "CNA Indonesia": False,
        "Jakarta Utara": True
    }
)