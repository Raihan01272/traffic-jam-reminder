from scraper import detik_articles
from test_cna_rss import cna_articles
from dummy_scraper import dummy_articles

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
    "plumpang"
]

def classify_location(text):
    text = text.lower()

    if any(
        keyword in text
        for keyword in main_location_keywords
    ):
        return "MAIN"

    elif any(
        keyword in text
        for keyword in nearby_location_keywords
    ):
        return "NEARBY"

    else:
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

all_articles = []

all_articles.extend(detik_articles)
all_articles.extend(cna_articles)
all_articles.extend(dummy_articles)

unique_articles = []
seen_urls = set()

for article in all_articles:
    article_url = article["link"]

    if article_url not in seen_urls:
        unique_articles.append(article)
        seen_urls.add(article_url)

print("\n=== DEDUPLICATION TEST ===")
print("Before Deduplication:", len(all_articles))
print("After Deduplication:", len(unique_articles))
print("Duplicate Articles:", len(all_articles) - len(unique_articles))

for article in unique_articles:
    text = (
        article["title"] + " " +
        article["description"]
    )

    article["location_category"] = classify_location(text)
    article["incident_category"] = classify_incident(text)

print("\n=== MULTI SOURCE DATA TEST ===")

print("Total Detik Articles:", len(detik_articles))
print("Total CNA Articles:", len(cna_articles))
print("Total Dummy Articles:", len(dummy_articles))
print("Total Combined Articles:", len(all_articles))

print("\n=== DATA TYPE INSPECTION ===")

print("Type of all_articles:", type(all_articles))

print("\nFirst Detik data:")
print("Type:", type(detik_articles[0]))
print(detik_articles[0])

print("\nFirst CNA data:")
print("Type:", type(cna_articles[0]))
print(cna_articles[0])

print("\n=== SOURCE DISTRIBUTOR ===")

source_counts = {}

for article in all_articles:
    source = article["source"]

    if source not in source_counts:
        source_counts[source] = 0

    source_counts[source] += 1

for source, total in source_counts.items():
    print(source, ":", total)

print("\n=== FIRST COMBINED ARTICLE ===")

if all_articles:
    print(all_articles[0])

valid_articles = []
invalid_articles = 0

for article in unique_articles:
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

        print("\n=== INVALID ARTICLE FOUND ===")
        print(article)

print("\n=== FINAL DATA VALIDATION ===")
print("Valid Articles:", len(valid_articles))
print("Invalid Articles:", invalid_articles)

def should_alert(location, incident):
    return location == "MAIN" and incident in [
        "TAWURAN",
        "DEMO",
        "KECELAKAAN_DAN_MACET"
    ]

alert_articles = []

for article in valid_articles:
    if should_alert(
        article["location_category"],
        article["incident_category"]
    ):
        alert_articles.append(article)

print("\n=== ALERT FILTERING TEST ===")

print("Total Articles Requiring Alert:", len(alert_articles))

for article in alert_articles:
    print("\nSource:", article["source"])
    print("Title:", article["title"])
    print("Location:", article["location_category"])
    print("Incident:", article["incident_category"])
    print("Link:", article["link"])
    print("-" * 50)

print("\n=== ARTICLE FILTERING RESULT ===")
print("Total Valid Articles:", len(valid_articles))
print("Articles Requiring Alert:", len(alert_articles))
print("Articles Not Requiring Alert:", len(valid_articles) - len(alert_articles))

sample_articles = [
    {
        "title": "Tawuran terjadi di Tanjung Priok",
        "location_category": "MAIN",
        "incident_category": "TAWURAN"
    },
    {
        "title": "Demo berlangsung di Bandung",
        "location_category": "NOT_RELEVANT",
        "incident_category": "DEMO"
    },
    {
        "title": "Kecelakaan di kawasan Koja",
        "location_category": "NEARBY",
        "incident_category": "NONE"
    }
]

print("\n=== FILTERING SIMULATION TEST ===")

for article in sample_articles:
    result = should_alert(
        article["location_category"],
        article["incident_category"]
    )

    print("Title:", article["title"])
    print("Alert:", result)
    print("-" * 40)

print("\n=== INCIDENT CLASSIFICATION TEST ===")

test_cases = [
    {
        "text": "Terjadi tawuran di Tanjung Priok",
        "location": "MAIN"
    },
    {
        "text": "Massa menggelar demonstrasi di Tanjung Priok",
        "location": "MAIN"
    },
    {
        "text": "Kecelakaan menyebabkan kemacetan di Tanjung Priok",
        "location": "MAIN"
    },
    {
        "text": "Kecelakaan terjadi di Tanjung Priok",
        "location": "MAIN"
    },
    {
        "text": "Tawuran terjadi di Bandung",
        "location": "NOT_RELEVANT"
    }
]

for test in test_cases:
    incident = classify_incident(test["text"])

    alert = should_alert(
        test["location"],
        incident
    )

    print("\nText:", test["text"])
    print("Incident:", incident)
    print("Alert:", alert)

print("\n=== LOCATION DISTIBUTION ===")

location_counts = {}

for article in unique_articles:
    location = article["location_category"]

    if location not in location_counts:
        location_counts[location] = 0

    location_counts[location] += 1

for location, total in location_counts.items():
    print(location, ":", total)

print("\n=== LOCATION KEYWORD TEST ===")

test_texts = [
    "Terjadi tawuran di Tanjung Priok",
    "Kemacetan di kawasan Koja",
    "Kecelakaan di Jalan Yos Sudarso",
    "Demo berlangsung di Pelabuhan Tanjung Priok",
    "Kepadatan lalu lintas di Sunter"
]

for text in test_texts:
    result = classify_location(text)

    print("Text:", text)
    print("Location:", result)
    print("-" * 40)

print("\n=== SAMPLE LOCATION CLASSIFICATION ===")

for article in all_articles[:10]:
    text = (
        article["title"] + " " +
        article["description"]
    )

    print("Source:", article["source"])
    print("Title:", article["title"])
    print("Description:", article["description"])
    print("Location:", classify_location(text))
    print("-" * 50)