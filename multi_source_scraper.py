from scrapers.scraper import fetch_detik_articles
from scrapers.test_cna_rss import fetch_cna_articles
from scrapers.dummy_scraper import fetch_dummy_articles
from scrapers.jakarta_utara_scraper import fetch_jakarta_utara_articles
from datetime import datetime
from datetime import datetime, timezone, timedelta

def is_fresh_article(article, hours=24):
    """
    Memeriksa apakah artikel diterbitkan dalam 24 jam terakhir.
    """

    published_at = article.get("published_at")

    # Artikel tanpa tanggal tidak dianggap fresh
    if not isinstance(published_at, datetime):
        return False

    # Artikel tanpa informasi zona waktu tidak dianggap fresh
    if published_at.tzinfo is None:
        return False

    # Waktu sekarang dalam UTC
    now_utc = datetime.now(timezone.utc)

    # Konversi tanggal publikasi ke UTC
    published_at_utc = published_at.astimezone(timezone.utc)

    # Hitung usia artikel
    article_age = now_utc - published_at_utc

    # Artikel harus berusia antara 0 dan 24 jam
    return timedelta(0) <= article_age <= timedelta(hours=hours)

main_location_keywords = [
    "tanjung priok",
    "priok",
    "kampung bahari",
    "yos sudarso",
    "re martadinata",
    "pelabuhan tanjung priok",
    "jalan bugis"
]

nearby_location_keywords = [
    "koja",
    "sunter",
    "warakas",
    "papanggo",
    "cilincing",
    "plumpang",
    "sungai bambu"
]


def classify_location(text):
    text = text.lower()

    for keyword in main_location_keywords:
        if keyword in text:
            return "MAIN"

    for keyword in nearby_location_keywords:
        if keyword in text:
            return "NEARBY"

    return "NOT_RELEVANT"

tawuran_keywords = [
    "tawuran",
    "bentrok",
    "keributan"
]

demo_keywords = [
    "demo",
    "demonstrasi",
    "unjuk rasa"
]

accident_keywords = [
    "kecelakaan",
    "tabrakan",
    "laka lantas"
]

traffic_keywords = [
    "macet",
    "kemacetan",
    "kepadatan",
    "lalu lintas",
    "antrean",
    "antrian"
]

road_disruption_keywords = [
    "jalan terendam",
    "jalan ditutup",
    "penutupan jalan",
    "akses jalan terganggu",
    "jalan tidak bisa dilalui",
    "pohon tumbang menutup jalan",
    "banjir menghambat lalu lintas",
    "genangan menghambat lalu lintas",
    "arus lalu lintas terganggu",
    "lalu lintas terganggu",
    "kendaraan tidak bisa melintas",
    "mengatur lalu lintas",
    "mengatur arus lalu lintas",
    "jalan mengalami genangan",
    "genangan di jalan",
    "jalan terdapat genangan"
]

road_impact_keywords = [
    "lalu lintas",
    "arus kendaraan",
    "jalan",
    "akses jalan",
    "kendaraan",
    "pengendara",
    "arus lalu lintas"
]

weather_disruption_keywords = [
    "banjir",
    "genangan",
    "jalan tergenang",
    "pohon tumbang",
    "hujan lebat",
    "hujan deras"
]


def classify_incident(text):

    text = text.lower()

    if any(keyword in text for keyword in tawuran_keywords):
        return "TAWURAN"

    elif any(keyword in text for keyword in demo_keywords):
        return "DEMO"

    elif (
        any(keyword in text for keyword in accident_keywords)
        and any(keyword in text for keyword in traffic_keywords)
    ):
        return "KECELAKAAN_DAN_MACET"

    elif any(keyword in text for keyword in road_disruption_keywords):
        return "GANGGUAN_JALAN"

    elif (
        any(keyword in text for keyword in weather_disruption_keywords)
        and any(keyword in text for keyword in road_impact_keywords)
    ):
        return "INDIKASI_GANGGUAN_JALAN"

    else:
        return "NONE"


def should_alert(location, incident):
    return location == "MAIN" and incident in [
        "TAWURAN",
        "DEMO",
        "KECELAKAAN_DAN_MACET",
        "GANGGUAN_JALAN"
    ]


def run_multi_source_pipeline():

    (
        detik_articles,
        detik_filtered,
        detik_total,
        detik_location,
        detik_traffic,
        detik_success,
        detik_error
    ) = fetch_detik_articles()


    (
        cna_articles,
        cna_response,
        cna_error,
        cna_success
    ) = fetch_cna_articles()

    dummy_articles = fetch_dummy_articles()

    (
        jakarta_utara_articles,
        jakarta_utara_success,
        jakarta_utara_error
    ) = fetch_jakarta_utara_articles()


    all_articles = []

    all_articles.extend(detik_articles)
    all_articles.extend(cna_articles)
    all_articles.extend(dummy_articles)
    all_articles.extend(jakarta_utara_articles)


    valid_articles = []
    invalid_articles = 0

    for article in all_articles:

        if (
            isinstance(article, dict)
            and article.get("source")
            and article.get("title")
            and article.get("description") is not None
            and article.get("link")
        ):
            valid_articles.append(article)

        else:
            invalid_articles += 1


    unique_articles = []
    seen_urls = set()

    for article in valid_articles:

        article_url = article["link"]

        if article_url not in seen_urls:

            unique_articles.append(article)
            seen_urls.add(article_url)


    duplicate_articles = len(valid_articles) - len(unique_articles)

    print("\n=== AUDIT PUBLISHED AT ===")

    for source_name in [
        "Detik.com",
        "CNA Indonesia",
        "Jakarta Utara",
        "Dummy News"
    ]:

        source_articles = [
            article
            for article in unique_articles
            if article.get("source") == source_name
        ]

        valid_dates = 0
        missing_dates = 0
        invalid_dates = 0

        for article in source_articles:

            published_at = article.get("published_at")

            if published_at is None:
                missing_dates += 1

            elif isinstance(published_at, datetime):
                valid_dates += 1

            else:
                invalid_dates += 1

        print(f"\nSumber: {source_name}")
        print("Total artikel:", len(source_articles))
        print("Tanggal valid:", valid_dates)
        print("Tanggal kosong:", missing_dates)
        print("Tipe tanggal tidak sesuai:", invalid_dates)


    for article in unique_articles:

        location_text = article["title"]
        incident_text = (
            article["title"] + " " +
            article["description"]
        )

        article["location_category"] = classify_location(location_text)
        article["incident_category"] = classify_incident(incident_text)

    print("\n=== AUDIT ARTIKEL FRESH DETIK.COM ===")

    fresh_detik_articles = [
        article
        for article in unique_articles
        if (
            article.get("source") == "Detik.com"
            and is_fresh_article(article, hours=24)
        )
    ]

    print("Total artikel fresh Detik.com:", len(fresh_detik_articles))

    for article in fresh_detik_articles:

        if (
            article["location_category"] == "MAIN"
            or article["incident_category"] != "NONE"
        ):
            print("\nJudul:", article["title"])
            print("Tanggal:", article["published_at"])
            print("Lokasi:", article["location_category"])
            print("Kejadian:", article["incident_category"])
            print("Link:", article["link"])
            print("-" * 60)

    print("\n=== DEBUG ARTIKEL TANJUNG PRIOK ===")

    for article in all_articles:
        if "Cuaca Ekstrem" in article["title"]:
            print("Judul:", article["title"])
            print("Deskripsi:", article["description"])
            print("Kategori lokasi:", article["location_category"])
            print("Kategori kejadian:", article["incident_category"])

    alert_articles = []

    for article in unique_articles:

        if article.get("source") == "Dummy News":
            continue

        if not is_fresh_article(article, hours=24):
            continue

        if should_alert(
            article["location_category"],
            article["incident_category"]
        ):
            alert_articles.append(article)

    print("\n=== FRESHNESS FILTER ===")
    print("Batas usia artikel: 24 jam")
    print("Total kandidat notifikasi:", len(alert_articles))

    for article in alert_articles:
        print("\nJudul:", article["title"])
        print("Sumber:", article["source"])
        print("Tanggal:", article["published_at"])

    print("\n=== FRESHNESS BREAKDOWN BY SOURCE ===")

    for source_name in [
        "Detik.com",
        "CNA Indonesia",
        "Jakarta Utara",
        "Dummy News"
    ]:

        source_articles = [
            article
            for article in unique_articles
            if article.get("source") == source_name
        ]

        fresh_count = sum(
            1
            for article in source_articles
            if is_fresh_article(article, hours=24)
        )

        print(f"\nSumber: {source_name}")
        print("Total artikel:", len(source_articles))
        print("Artikel fresh:", fresh_count)
        print("Artikel lama/tidak valid:", len(source_articles) - fresh_count)

    all_sources_success = (
        detik_success
        and cna_success
        and jakarta_utara_success
    )

    return {
        "detik_articles": detik_articles,
        "cna_articles": cna_articles,
        "dummy_articles": dummy_articles,
        "all_articles": all_articles,
        "valid_articles": valid_articles,
        "unique_articles": unique_articles,
        "alert_articles": alert_articles,
        "invalid_articles": invalid_articles,
        "duplicate_articles": duplicate_articles,
        "detik_filtered": detik_filtered,
        "detik_total": detik_total,
        "detik_location": detik_location,
        "detik_traffic": detik_traffic,
        "detik_success": detik_success,
        "detik_error": detik_error,
        "cna_response": cna_response,
        "cna_error": cna_error,
        "cna_success": cna_success,
        "jakarta_utara_articles": jakarta_utara_articles,
        "jakarta_utara_success": jakarta_utara_success,
        "jakarta_utara_error": jakarta_utara_error,
        "all_sources_success": all_sources_success,
    }



if __name__ == "__main__":

    results = run_multi_source_pipeline()

    print("\n" + "=" * 60)
    print("TRAFFIC JAM REMINDER - TANJUNG PRIOK")
    print("=" * 60)

    print("\n[1] SOURCE HEALTH")
    print("-" * 60)

    print("Overall Status:", results["all_sources_success"])

    print("Detik.com:")
    print("  Status:", results["detik_success"])
    print("  Error :", results["detik_error"])

    print("CNA Indonesia:")
    print("  Status:", results["cna_success"])
    print("  Error :", results["cna_error"])

    print("Jakarta Utara:")
    print("  Status:", results["jakarta_utara_success"])
    print("  Error :", results["jakarta_utara_error"])

    print("Dummy News:")
    print("  Status: TEST DATA ONLY")


    print("\n[2] DATA COLLECTION")
    print("-" * 60)

    print("Detik.com       :", len(results["detik_articles"]))
    print("CNA Indonesia   :", len(results["cna_articles"]))
    print("Dummy News      :", len(results["dummy_articles"]))
    print("Jakarta Utara   :", len(results["jakarta_utara_articles"]))
    print("Total Articles  :", len(results["all_articles"]))


    print("\n[3] DATA CLEANING AND VALIDATION")
    print("-" * 60)

    print("Before Deduplication :", len(results["valid_articles"]))
    print("After Deduplication  :", len(results["unique_articles"]))
    print("Duplicates Removed   :", results["duplicate_articles"])

    print("Valid Articles       :", len(results["valid_articles"]))
    print("Invalid Articles     :", results["invalid_articles"])


    print("\n[4] SOURCE DISTRIBUTION")
    print("-" * 60)

    source_counts = {}

    for article in results["unique_articles"]:
        source = article["source"]
        source_counts[source] = source_counts.get(source, 0) + 1

    for source, total in source_counts.items():
        print(f"{source:<20}: {total}")


    print("\n[5] LOCATION CLASSIFICATION")
    print("-" * 60)

    location_counts = {
        "MAIN": 0,
        "NEARBY": 0,
        "NOT_RELEVANT": 0
    }

    for article in results["unique_articles"]:
        location = article["location_category"]
        location_counts[location] = location_counts.get(location, 0) + 1

    print("Tanjung Priok (MAIN) :", location_counts["MAIN"])
    print("Nearby Areas         :", location_counts["NEARBY"])
    print("Not Relevant         :", location_counts["NOT_RELEVANT"])

    print("\n[5B] RELEVANT ARTICLE DETAILS")
    print("-" * 60)

    for category in ["MAIN", "NEARBY"]:

        print(f"\n--- {category} ARTICLES ---")

        relevant_articles = [
            article
            for article in results["unique_articles"]
            if article["location_category"] == category
        ]

        if not relevant_articles:
            print("Tidak ada berita ditemukan.")
            continue

        for index, article in enumerate(relevant_articles, start=1):

            print(f"\n{index}. {article['title']}")
            print("   Source   :", article["source"])
            print("   Incident :", article["incident_category"])
            print("   Link     :", article["link"])

    print("\n" + "-" * 60)
    print("END OF RELEVANT ARTICLE DETAILS")

    print("\nJakarta Utara Article Review:")

    jakarta_articles = results["jakarta_utara_articles"]

    jakarta_location_counts = {
        "MAIN": 0,
        "NEARBY": 0,
        "NOT_RELEVANT": 0
    }

    for article in jakarta_articles:
        location = classify_location(article["title"])

        jakarta_location_counts[location] += 1

    print("Total Articles       :", len(jakarta_articles))
    print("Tanjung Priok        :", jakarta_location_counts["MAIN"])
    print("Nearby Areas         :", jakarta_location_counts["NEARBY"])
    print("Not Relevant         :", jakarta_location_counts["NOT_RELEVANT"])


    print("\n[6] INCIDENT CLASSIFICATION")
    print("-" * 60)

    print("\n" + "-" * 60)

    incident_counts = {}

    for article in results["unique_articles"]:
        incident = article["incident_category"]
        incident_counts[incident] = incident_counts.get(incident, 0) + 1

    for incident, total in incident_counts.items():
        print(f"{incident:<25}: {total}")

    print("\n[6B] INCIDENT BREAKDOWN BY SOURCE")
    print("-" * 60)

    incident_types = [
        "TAWURAN",
        "DEMO",
        "KECELAKAAN_DAN_MACET",
        "GANGGUAN_JALAN",
        "INDIKASI_GANGGUAN_JALAN"
    ]

    source_incident_counts = {}

    for article in results["unique_articles"]:

        source = article["source"]
        incident = article["incident_category"]

        if source not in source_incident_counts:
            source_incident_counts[source] = {
                incident_type: 0
                for incident_type in incident_types
            }

        if incident in incident_types:
            source_incident_counts[source][incident] += 1

    for source, counts in source_incident_counts.items():

        print(f"\n{source}")

        for incident_type in incident_types:
            print(
                f"  {incident_type:<25}: "
                f"{counts[incident_type]}"
            )


    print("\n[7] ALERT FILTERING")
    print("-" * 60)

    alert_articles = results["alert_articles"]

    dummy_alerts = [
        article for article in alert_articles
        if article["source"] == "Dummy News"
    ]

    real_alerts = [
        article for article in alert_articles
        if article["source"] != "Dummy News"
    ]

    print("Total Valid Articles       :", len(results["valid_articles"]))
    print("Total Alert Candidates     :", len(alert_articles))
    print("Articles Not Requiring Alert:",
          len(results["unique_articles"]) - len(alert_articles))

    print("Real Source Alerts         :", len(real_alerts))
    print("Dummy Test Alerts          :", len(dummy_alerts))


    if alert_articles:
        print("\nAlert Candidate Details:")

        for article in alert_articles:
            print("\nSource   :", article["source"])
            print("Title    :", article["title"])
            print("Location :", article["location_category"])
            print("Incident :", article["incident_category"])
            print("Link     :", article["link"])
            print("-" * 60)


    print("\n[8] INCIDENT CLASSIFICATION TEST")
    print("-" * 60)

    test_cases = [
        "Terjadi tawuran di Tanjung Priok",
        "Massa menggelar demonstrasi di Tanjung Priok",
        "Kecelakaan menyebabkan kemacetan di Tanjung Priok",
        "Kecelakaan terjadi di Tanjung Priok",
        "Tawuran terjadi di Bandung",
        "Banjir menyebabkan jalan Tanjung Priok terendam dan lalu lintas terganggu",
        "Banjir melanda permukiman Tanjung Priok",
        "Genangan terjadi di sejumlah titik Tanjung Priok",
        "Pohon tumbang di jalan Tanjung Priok",
        "Hujan lebat menyebabkan banjir di Tanjung Priok",
        "Jalan Tanjung Priok terendam dan lalu lintas terganggu",
        "Petugas mengatur lalu lintas akibat pohon tumbang di Jalan Bugis",
        "Genangan air terjadi di Jalan Cilincing Lama dengan ketinggian 6 cm",
        "Petugas memeriksa pompa dan membersihkan saluran untuk kesiapsiagaan banjir"
    ]

    for text in test_cases:
        location = classify_location(text)
        incident = classify_incident(text)
        alert = should_alert(location, incident)

        print("\nText     :", text)
        print("Location :", location)
        print("Incident :", incident)
        print("Alert    :", alert)

    print("\n" + "=" * 60)
    print("PIPELINE REPORT COMPLETED")
    print("=" * 60)