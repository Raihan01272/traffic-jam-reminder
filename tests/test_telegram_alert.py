from datetime import datetime
from zoneinfo import ZoneInfo

from notifications.telegram_notifier import (
    send_telegram_notifications
)


sample_article = {
    "source": "Detik.com",

    "title": (
        "Simulasi: Genangan Air Mengganggu "
        "Arus Lalu Lintas di Tanjung Priok"
    ),

    "description": (
        "Artikel simulasi untuk menguji notifikasi "
        "gangguan jalan di Tanjung Priok."
    ),

    "link": (
        "https://example.com/"
        "simulasi-gangguan-tanjung-priok"
    ),

    "location_category": "MAIN",

    "incident_category": "GANGGUAN_JALAN",

    "published_at": datetime.now(
        ZoneInfo("Asia/Jakarta")
    )
}

test_alert_articles = [
    sample_article
]


print("=== PENGUJIAN TELEGRAM ALERT ===")

send_telegram_notifications(
    alert_articles=test_alert_articles,
    all_sources_success=True,
    dry_run=True
)