from notifications.telegram_notifier import (
    send_telegram_notifications
)

print("=== PENGUJIAN SUMBER BERITA GAGAL ===")

send_telegram_notifications(
    alert_articles=[],
    all_sources_success=False,
    dry_run=True,
    source_status={
        "Detik.com": True,
        "CNA Indonesia": False,
        "Jakarta Utara": True
    }
)