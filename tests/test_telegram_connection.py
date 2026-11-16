import os
import requests

from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent

load_dotenv(project_root / ".env")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

if not bot_token or not chat_id:
    print("Token atau Chat ID belum dikonfigurasi.")
    raise SystemExit

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": (
        "🚦 TEST TRAFFIC JAM REMINDER\n\n"
        "Koneksi Telegram berhasil!\n"
        "Traffic Jam Reminder Tanjung Priok siap diuji."
    )
}

try:
    response = requests.post(
        url,
        data=payload,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    if result.get("ok"):
        print("Berhasil! Pesan percobaan sudah dikirim.")
    else:
        print("Telegram menolak pesan:", result)

except requests.exceptions.RequestException as error:
    print("Koneksi gagal:", error)
