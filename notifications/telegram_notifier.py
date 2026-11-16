import os
import requests

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from notifications.notification_manager import (
    is_article_sent,
    save_sent_article
)


JAKARTA_TIMEZONE = ZoneInfo("Asia/Jakarta")

def get_incident_reason(incident_category):

    incident_reasons = {
        "TAWURAN": "Terjadi laporan tawuran.",
        "DEMO": "Terjadi laporan demonstrasi.",
        "KECELAKAAN_DAN_MACET": "Terjadi laporan kecelakaan dan kemacetan.",
        "GANGGUAN_JALAN": "Terjadi laporan gangguan jalan."
    }

    return incident_reasons.get(
        incident_category,
        "Terdapat laporan gangguan lalu lintas."
    )


def format_published_date(published_at):

    if not isinstance(published_at, datetime):
        return "Tanggal publikasi tidak tersedia"

    if published_at.tzinfo is None:
        return "Tanggal publikasi tidak valid"

    jakarta_time = published_at.astimezone(JAKARTA_TIMEZONE)

    return jakarta_time.strftime("%d-%m-%Y %H:%M WIB")


def format_alert_article(article):

    incident_reason = get_incident_reason(
        article.get("incident_category")
    )

    published_date = format_published_date(
        article.get("published_at")
    )

    return (
        f"Sumber: {article['source']}\n"
        f"Judul: {article['title']}\n"
        f"Kategori: {incident_reason}\n"
        f"Waktu: {published_date}\n"
        f"Lokasi: {article.get('location_category', 'Tidak diketahui')}\n"
        f"Link: {article['link']}\n\n"
    )


def send_telegram_notifications(
    alert_articles,
    all_sources_success,
    dry_run=False,
    source_status=None
):

    real_alert_articles = [
        article for article in alert_articles
        if article.get("source") != "Dummy News"
    ]


    new_alert_articles = []

    alerts_included_in_message = False

    for article in real_alert_articles:

        article_link = article["link"]

        if is_article_sent(article_link):

            print(
                "Berita sudah pernah dikirim:",
                article["title"]
            )

        else:

            new_alert_articles.append(article)


    if not all_sources_success:

        failed_sources = []

        if source_status:

            for source, success in source_status.items():

                if not success:
                    failed_sources.append(source)

        if failed_sources:

            failure_details = "\n".join(
                f"- {source}: gagal diakses"
                for source in failed_sources
            )

        else:

            failure_details = (
                "- Terdapat sumber berita yang gagal diakses."
            )

        message = (
            "⚠️ INFORMASI LALU LINTAS TANJUNG PRIOK\n\n"
            "Status: PEMANTAUAN TIDAK LENGKAP\n\n"
            "Alasan:\n"
            f"{failure_details}\n\n"
            "Status lalu lintas belum dapat dipastikan "
            "karena tidak seluruh sumber berita berhasil diakses."
        )

        print("PERINGATAN: Pemantauan tidak lengkap.")


    elif new_alert_articles:

        message = (
            "🚨 INFORMASI LALU LINTAS TANJUNG PRIOK\n\n"
            "Status: ADA LAPORAN GANGGUAN\n\n"
        )

        included_articles = []

        for article in new_alert_articles:

            article_message = format_alert_article(article)

            if len(message) + len(article_message) > 3900:
                print(
                    "Artikel tidak dimasukkan karena batas panjang pesan:",
                    article["title"]
                )
                continue

            message += article_message

            included_articles.append(article)

        if included_articles:
            alerts_included_in_message = True

        else:
            print("Tidak ada artikel yang dapat dimasukkan ke pesan Telegram.")
            return


    elif real_alert_articles:

        print(
            "Tidak ada berita alert baru. "
            "Notifikasi tidak dikirim."
        )

        return


    elif alert_articles:

        print(
            "Alert hanya berasal dari Dummy News. "
            "Notifikasi tidak dikirim."
        )

        return


    else:

        message = (
            "🚦 INFORMASI LALU LINTAS TANJUNG PRIOK\n\n"
            "Status: BELUM DITEMUKAN LAPORAN GANGGUAN\n\n"
            "Belum ditemukan laporan gangguan lalu lintas "
            "di wilayah Tanjung Priok berdasarkan artikel "
            "yang berhasil dipantau.\n\n"
            "Catatan: Ini bukan jaminan bahwa seluruh jalan "
            "sedang lancar."
        )


    if dry_run:

        print("\n=== DRY RUN MODE ===")
        print("Pesan yang seharusnya dikirim:")
        print()
        print(message)
        print()
        print("Simulasi selesai. Tidak ada pesan yang dikirim.")

        return

    project_root = Path(__file__).resolve().parent.parent

    load_dotenv(project_root / ".env")

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:

        print(
            "ERROR: TELEGRAM_BOT_TOKEN atau "
            "TELEGRAM_CHAT_ID belum dikonfigurasi."
        )

        return


    telegram_url = (
        f"https://api.telegram.org/bot{bot_token}/sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": True
    }

    try:

        response = requests.post(
            telegram_url,
            data=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if result.get("ok"):

            print("Notifikasi Telegram berhasil dikirim.")

            if alerts_included_in_message:

                for article in included_articles:

                    save_sent_article(
                        article["link"],
                        article["title"]
                    )

        else:

            print(
                "Telegram gagal mengirim pesan:",
                result
            )

    except requests.exceptions.RequestException as error:

        print(
            "ERROR saat mengirim notifikasi Telegram:",
            error
        )