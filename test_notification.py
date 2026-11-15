from telegram_notifier import send_telegram_notifications

print("\n=== TEST 1: SEMUA SUMBER BERHASIL, ADA ALERT ===")

dummy_alert = [
    {
        "source": "Detik.com",
        "title": "Tawuran di Tanjung Priok",
        "link": "https://example.com/test-alert"
    }
]

send_telegram_notifications(
    dummy_alert,
    True,
    dry_run=True
)


print("\n=== TEST 2: SEMUA SUMBER BERHASIL, TIDAK ADA ALERT ===")

send_telegram_notifications(
    [],
    True,
    dry_run=True
)


print("\n=== TEST 3: ADA SUMBER GAGAL ===")

send_telegram_notifications(
    [],
    False,
    dry_run=True
)

print("\n=== TEST 4: ALERT DARI SUMBER BERITA ASLI ===")

real_alert = [
    {
        "source": "Detik.com",
        "title": "Tawuran Terjadi di Tanjung Priok",
        "link": "https://example.com/test-real-alert"
    }
]

send_telegram_notifications(
    real_alert,
    True,
    dry_run=True
)

print("\n=== TEST 5: ADA ALERT, TETAPI SALAH SATU SUMBER GAGAL ===")

real_alert_source_failed = [
    {
        "source": "Detik.com",
        "title": "Tawuran Terjadi di Tanjung Priok",
        "link": "https://example.com/test-source-failed"
    }
]

send_telegram_notifications(
    real_alert_source_failed,
    False,
    dry_run=True
)