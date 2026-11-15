import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

url = "https://news.detik.com/berita/rss"

response = requests.get(url, timeout=30)
response.raise_for_status()

root = ET.fromstring(response.content)
channel = root.find("channel")
articles = channel.findall("item")

print("Total Articles:", len(articles))

main_location_keywords = [
    "tanjung priok",
    "priok",
    "kampung bahari",
    "yos sudarso",
    "re martadinata",
    "pelabuhan tanjung priok",
]

nearby_location_keywords = [
    "koja",
    "sunter",
    "warakas",
    "papanggo",
    "cilincing",
    "plumpang",
]

location_keywords = main_location_keywords + nearby_location_keywords

traffic_keywords = [
    "congestion",
    "traffic jam",
    "queue",
    "macet",
    "kemacetan",
    "antrian",
    "antrean",
    "padat",
    "mengantre",
    "kepadatan",
    "lalu lintas",
]

test_locations = [
    "Kemacetan terjadi di Tanjung Priok",
    "Kendaraan padat di Jalan Yos Sudarso",
    "Kepadatan lalu lintas di Koja",
    "Kecelakaan terjadi di Sunter",
    "Banjir melanda kawasan Plumpang",
    "Kemacetan terjadi di Bandung",
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

def classify_traffic_article(text):
    text = text.lower()

    is_traffic = any(
        re.search(
            r"\b" + re.escape(keyword) + r"\b",
            text
        )
        for keyword in traffic_keywords
    )

    if is_traffic:
        return True
    else:
        return False

def is_relevant_article(text):
    location = classify_location(text)
    traffic = classify_traffic_article(text)

    if location in ["MAIN", "NEARBY"] and traffic:
        return True
    else:
        return False

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    clean_text = soup.get_text(
        separator = " ",
        strip=True
    )

    return clean_text

print("\n=== HTML CLEANING TEST ===")

sample_html = """
<img src="image.jpg"/>
Kemacetan terjadi di Jalan Yos Sudarso.
<b>Kendaraan mengantre panjang.</b>
"""

cleaned_text = clean_html(sample_html)

print("Before:", sample_html)
print("After:", cleaned_text)

print("=== RELEVANT ARTICLE TEST")

test_articles = [
    "Kemacetan terjadi di Tanjung Priok",
    "Kendaraan padat di Jalan Yos Sudarso",
    "Kepadatan lalu lintas di Koja",
    "Penataan Kampung Bahari berlanjut",
    "Kecelakaan terjadi di Sunter",
    "Kemacetan terjadi di Bandung",
]

for text in test_articles:
    result = is_relevant_article(text)
    print(text, "=>", result)

print("\n=== ARTICLE CLASSIFICATION TEST ===")

test_articles = [
    "Kemacetan terjadi di Tanjung Priok",
    "Kendaraan padat di Jalan Yos Sudarso",
    "Kepadatan lalu lintas di Koja",
    "Penataan Kampung Bahari berlanjut",
    "Kecelakaan terjadi di Sunter",
]

for text in test_articles:
    location_result = classify_location(text)
    traffic_result = classify_traffic_article(text)

    print(
        text,
        "=> Location:", location_result,
        "| Traffic:", traffic_result
    )

print("\n=== LOCATION KEYWORD TEST ===")

test_locations = [
    "Kemacetan terjadi di Tanjung Priok",
    "Kendaraan padat di Jalan Yos Sudarso",
    "Kepadatan lalu lintas di Koja",
    "Kecelakaan terjadi di Sunter",
    "Kemacetan terjadi di Bandung",
]

for text in test_locations:
    result = classify_location(text)
    print(text, "=>", result)

for text in test_locations:
    text = text.lower()

    is_main_location = any(
        keyword in text
        for keyword in main_location_keywords
    )

    is_nearby_location = any(
        keyword in text
        for keyword in nearby_location_keywords
    )

    print(
        text,
        "=> Main:", is_main_location,
        "| Nearby:", is_nearby_location
    )

filtered_articles = []

location_matches = 0
traffic_matches = 0

for article in articles:
    title = article.findtext("title", default="")
    raw_description = article.findtext("description", default="")
    description = clean_html(raw_description)
    link = article.findtext("link", default="")

    text = f"{title} {description}".lower()

    location_category = classify_location(text)

    is_traffic = classify_traffic_article(text)

    if location_category in ["MAIN", "NEARBY"]:
        location_matches += 1

    if is_traffic:
        traffic_matches += 1

        print("\n=== TRAFFIC MATCH DETAILS ===")
        print("Title:", title)
        print("Description:", description)
        print("-" * 50)

    if is_relevant_article(text):
        filtered_articles.append({
            "title": title,
            "description": description,
            "link": link,
            "location_category": location_category
        })

text_cases = [
    "Kemaren terjadi selama 2 jam",
    "Saya makan jamur",
    "Jalan yos sudarso macet",
    "Kondisi lalu lintas padat",
    "Pengendara mengantre panjang",
    "Kepadatan kendaraan meningkat",
]

for text in text_cases:
    result = any(
        re.search(
            r"\b" + re.escape(keyword) + r"\b",
            text.lower()
        )
        for keyword in traffic_keywords
    )

    print(text, "=>", result)
    
print("\n=== LOCATION MATCH DETAILS ===")

for article in articles:
    title = article.findtext("title", default ="")
    description = article.findtext("description", default ="")
    text = f"{title} {description}".lower()

    is_location_relevant = any(
        keyword in text
        for keyword in location_keywords
    )

    if is_location_relevant:
        print("Title:", title)
        print("Description:", description)
        print("-" * 50)

print("\n=== FILTER SUMMARY ===")
print("Location Matches:", location_matches)
print("Traffic Matches:", traffic_matches)
print("Relevant Articles:", len(filtered_articles))

print("\n=== RELEVANT ARTICLES ===")

for item in filtered_articles:
    print("Title:", item["title"])
    print("Location:", item["location_category"])
    print("Link:", item["link"])
    print("-" * 50)

print("\n=== DICTIONARY AND LIST TEST ===")

sample_article = {
    "title": "Kemacetan di Tanjung Priok",
    "description": "Kendaraan mengantre panjang di jalan Yos Sudarso",
    "link": "https://example.com/traffic",
    "location_category": "MAIN"
}

sample_articles = []

sample_articles.append(sample_article)

print("Article Title:", sample_articles[0]["title"])
print("Description:", sample_articles[0]["description"])
print("Location:", sample_articles[0]["location_category"])

print("Total Articles:", len(sample_articles))

print("\n=== RSS DATA STRUCTURE TEST ===")

print("Total Relevant Articles:", len(filtered_articles))

if filtered_articles:
    first_articles = filtered_articles[0]

    print("Title:", first_articles["title"])
    print("Description:", first_articles["description"])
    print("Location:", first_articles["location_category"])
    print("Link:", first_articles["link"])

else:
    print("No relevant articles found.")

print("\n=== MANUAL RSS DATA TEST ===")

test_article = {
    "title": "Kemacetan di Tanjung Priok",
    "description": " Kendaraan mengantre panjang di Jalan Yos Sudarso.",
    "link": "https://example/com/traffic",
    "location_category": "MAIN"
}

filtered_articles.append(test_article)

print("Total Relevant Articles:", len(filtered_articles))

for item in filtered_articles:
    print("Title:", item["title"])
    print("Description:", item["description"])
    print("Location:", item["location_category"])
    print("-" * 50)

print("\n=== FINAL FILTERING TEST ===")

test_cases = [
    {
        "title": "Kemacetan terjadi di Tanjung Priok",
        "expected": True
    },
    {
        "title": "Penataan Kampung Bahari berlanjut",
        "expected": False
    },
    {
       "title": "Kemacetan terjadi di Bandung",
        "expected": False
    }
]

for item in test_cases:
    result = is_relevant_article(item["title"])

    print(
        item["title"],
        "=> Actual:", result,
        "| Expected:", item["expected"]
    )