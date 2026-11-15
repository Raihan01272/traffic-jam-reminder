from scrapers.scraper import fetch_detik_articles
from scrapers.test_cna_rss import fetch_cna_articles
from scrapers.dummy_scraper import fetch_dummy_articles
from scrapers.jakarta_utara_scraper import fetch_jakarta_utara_articles

main_location_keywords = [
    "tanjung priok",
    "priok",
    "kampung bahari",
    "yos sudarso",
    "re martadinata",
    "pelabuhan tanjung priok"
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

    for keyword in nearby_location_keywords:
        if keyword in text:
            return "NEARBY"

    for keyword in main_location_keywords:
        if keyword in text:
            return "MAIN"

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

    else:
        return "NONE"


def should_alert(location, incident):

    return location == "MAIN" and incident in [
        "TAWURAN",
        "DEMO",
        "KECELAKAAN_DAN_MACET"
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


    for article in unique_articles:

        location_text = article["title"]

        incident_text = (
            article["title"] + " " +
            article["description"]
        )

        article["location_category"] = classify_location(location_text)
        article["incident_category"] = classify_incident(incident_text)

    alert_articles = []

    for article in unique_articles:

        if should_alert(
            article["location_category"],
            article["incident_category"]
        ):
            alert_articles.append(article)

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
        "KECELAKAAN_DAN_MACET"
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
        "Tawuran terjadi di Bandung"
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