from multi_source_scraper import run_multi_source_pipeline
from database.database import save_articles
from reports.export_to_excel import export_to_excel
from notifications.telegram_notifier import send_telegram_notifications


def main():

    print("================================")
    print("TRAFFIC JAM REMINDER")
    print("TANJUNG PRIOK")
    print("================================")

    print("\n1. Mengambil berita dari berbagai sumber...")

    results = run_multi_source_pipeline()

    real_valid_articles = [
        article
        for article in results["valid_articles"]
        if article["source"] != "Dummy News"
    ]

    print("\n2. Menyimpan artikel ke database...")

    total_articles = save_articles(real_valid_articles)

    print("Penyimpanan database selesai!")
    print("Artikel berhasil disimpan:", total_articles)


    print("\n3. Membuat laporan Excel...")

    total_excel = export_to_excel()

    print("Pembuatan laporan Excel selesai!")
    print("Baris laporan Excel:", total_excel)

    print("\n4. Memproses notifikasi Telegram...")

    real_alert_articles = [
        article
        for article in results["alert_articles"]
        if article["source"] != "Dummy News"
    ]

    print("\n=== DIAGNOSTIC REAL ARTICLES ===")

    for article in results["unique_articles"]:

        if (
            article["source"] != "Dummy News"
            and article["location_category"] == "MAIN"
        ):

            print("\nSource:", article["source"])
            print("Title:", article["title"])
            print("Description:", article["description"])
            print("Location:", article["location_category"])
            print("Incident:", article["incident_category"])
            print("Link:", article["link"])
            print("-" * 50)

    print("\nTotal real alert articles:", len(real_alert_articles))

    for article in real_alert_articles:
        print("Sumber notifikasi:", article["source"])

    source_status = {
        "Detik.com": results["detik_success"],
        "CNA Indonesia": results["cna_success"],
        "Jakarta Utara": results["jakarta_utara_success"]
    }

    dummy_only_alerts = (
        results["all_sources_success"]
        and results["alert_articles"]
        and not real_alert_articles
    )

    if dummy_only_alerts:

        print("\nAlert hanya berasal dari Dummy News.")
        print("Notifikasi Telegram tidak dikirim.")

    else:

        if not results["all_sources_success"]:

            print("\nPERINGATAN: Ada sumber berita yang gagal diakses.")

        print("\nMengirim notifikasi Telegram...")

        send_telegram_notifications(
            alert_articles=real_alert_articles,
            all_sources_success=results["all_sources_success"],
            dry_run=False,
            source_status=source_status
        )

    print("Proses notifikasi Telegram selesai!")


    print("\n=== SCRAPING RESULT ===")

    print("Detik Articles:", len(results["detik_articles"]))
    print("CNA Articles:", len(results["cna_articles"]))
    print("Dummy Articles:", len(results["dummy_articles"]))
    print("Jakarta Utara Articles:", len(results["jakarta_utara_articles"]))
    print("Total Articles:", len(results["all_articles"]))

    print("\n=== DATA VALIDATION ===")

    print("Valid Articles:", len(results["valid_articles"]))
    print("Real Valid Articles:", len(real_valid_articles))
    print("Invalid Articles:", results["invalid_articles"])
    print("Duplicate Articles:", results["duplicate_articles"])


    print("\n=== CLASSIFICATION RESULT ===")

    print("Unique Articles:", len(results["unique_articles"]))
    print("Articles Requiring Alert:", len(results["alert_articles"]))
    print("Real Alert Articles:", len(real_alert_articles))


    print("\n=== ALERT ARTICLES ===")

    if results["alert_articles"]:

        for article in results["alert_articles"]:

            print("\nSource:", article["source"])
            print("Title:", article["title"])
            print("Location:", article["location_category"])
            print("Incident:", article["incident_category"])
            print("Link:", article["link"])
            print("-" * 50)

    else:

        print("Tidak ditemukan artikel yang memenuhi syarat alert.")


    print("\nProses scraping dan klasifikasi selesai!")

    print("\n================================")
    print("TRAFFIC JAM REMINDER COMPLETED")
    print("================================")


if __name__ == "__main__":

    main()