from multi_source_scraper import run_multi_source_pipeline
from database import save_articles
from export_to_excel import export_to_excel
from telegram_notifier import send_telegram_notifications

def main():

    print("================================")
    print("TRAFFIC JAM REMINDER")
    print("TANJUNG PRIOK")
    print("================================")


    print("\n1. Mengambil berita dari berbagai sumber...")
    results = run_multi_source_pipeline()

    print("\n2. Menyimpan artikel ke database...")
    total_articles = save_articles(results["valid_articles"])

    print("Penyimpanan database selesai")

    print("\n3. Membuat laporan Excel...")

    total_excel = export_to_excel()

    print("Pembuatan laporan excel selesai!")

    print("\n4. Mengirim notifikasi Telegram...")

    real_alert_articles = [
        article
        for article in results["alert_articles"]
        if article["source"] != "Dummy News"
    ]

    print("Total real alert articles:", len(real_alert_articles))

    for article in real_alert_articles:
        print("Sumber notifikasi:", article["source"])

    if results["alert_articles"] and not real_alert_articles:
        print("Alert hanya berasal dari Dummy News.")
        print("Notifikasi Telegram tidak dikirim.")

    else:
        send_telegram_notifications(
            real_alert_articles,
            results["all_sources_success"],
            dry_run=True
        )

    print("Proses notifikasi Telegram selesai!")
    print("\n=== SCRAPING RESULT ===")

    print("Detik Articles:", len(results["detik_articles"]))
    print("CNA Articles:", len(results["cna_articles"]))
    print("Dummy Articles:", len(results["dummy_articles"]))

    print("Total Articles:", len(results["all_articles"]))


    print("\n=== DATA VALIDATION ===")

    print("Valid Articles:", len(results["valid_articles"]))
    print("Invalid Articles:", results["invalid_articles"])
    print("Duplicate Articles:", results["duplicate_articles"])


    print("\n=== CLASSIFICATION RESULT ===")

    print("Unique Articles:", len(results["unique_articles"]))
    print("Articles Requiring Alert:", len(results["alert_articles"]))


    print("\n=== ALERT ARTICLES ===")

    for article in results["alert_articles"]:

        print("\nSource:", article["source"])
        print("Title:", article["title"])
        print("Location:", article["location_category"])
        print("Incident:", article["incident_category"])
        print("Link:", article["link"])
        print("-" * 50)


    print("\nProses scraping dan klasifikasi selesai!")

if __name__ == "__main__":

    main()
