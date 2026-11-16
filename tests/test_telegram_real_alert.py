from datetime import datetime
from zoneinfo import ZoneInfo
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from notifications.telegram_notifier import (
    send_telegram_notifications
)
JAKARTA_TIMEZONE = ZoneInfo("Asia/Jakarta")

test_article = {
    "source": "Test News",
    "title": "Tawuran Terjadi di Tanjung Priok",
    "description": (
        "Simulasi laporan tawuran di kawasan "
        "Tanjung Priok untuk menguji notifikasi."
    ),
    "link": (
        "https://example.com/test-real-alert-20261116"
    ),
    "published_at": datetime.now(JAKARTA_TIMEZONE),
    "location_category": "MAIN",
    "incident_category": "TAWURAN"
}

print("=== PENGUJIAN NOTIFIKASI TELEGRAM ===")
print("Judul:", test_article["title"])
print("Lokasi:", test_article["location_category"])
print("Kategori:", test_article["incident_category"])

send_telegram_notifications(
    alert_articles=[test_article],
    all_sources_success=True,
    dry_run=False
)

print("\nPengujian selesai.")