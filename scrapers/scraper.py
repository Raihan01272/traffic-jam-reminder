
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from email.utils import parsedate_to_datetime

url = "https://news.detik.com/berita/rss"

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

    return is_traffic


def is_relevant_article(text):
    location = classify_location(text)
    traffic = classify_traffic_article(text)

    return location in ["MAIN", "NEARBY"] and traffic


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    clean_text = soup.get_text(
        separator=" ",
        strip=True
    )

    return clean_text


def fetch_detik_articles():

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        channel = root.find("channel")

        if channel is None:
            raise ValueError("RSS channel tidak ditemukan")

        articles = channel.findall("item")

        detik_articles = []
        filtered_articles = []

        location_matches = 0
        traffic_matches = 0

        for article in articles:

            title = article.findtext(
                "title",
                default=""
            ).strip()

            raw_description = article.findtext(
                "description",
                default=""
            )

            description = clean_html(raw_description)

            link = article.findtext(
                "link",
                default=""
            ).strip()

            # Mengambil tanggal publikasi dari RSS
            raw_published_at = article.findtext(
                "pubDate",
                default=""
            ).strip()

            # Mengubah teks tanggal menjadi datetime
            try:
                published_at = parsedate_to_datetime(
                    raw_published_at
                )

            except (TypeError, ValueError):
                published_at = None

            text = f"{title} {description}".lower()

            location_category = classify_location(text)
            is_traffic = classify_traffic_article(text)

            detik_article = {
                "source": "Detik.com",
                "title": title,
                "description": description,
                "link": link,
                "published_at": published_at,
                "location_category": location_category
            }

            detik_articles.append(detik_article)

            if location_category in ["MAIN", "NEARBY"]:
                location_matches += 1

            if is_traffic:
                traffic_matches += 1

            if is_relevant_article(text):
                filtered_articles.append(detik_article)

        return (
            detik_articles,
            filtered_articles,
            len(articles),
            location_matches,
            traffic_matches,
            True,
            None
        )

    except Exception as error:

        print("Detik RSS gagal diambil:", error)

        return (
            [],
            [],
            0,
            0,
            0,
            False,
            str(error)
        )


if __name__ == "__main__":

    (
        detik_articles,
        filtered_articles,
        total_articles,
        location_matches,
        traffic_matches,
        detik_success,
        detik_error
    ) = fetch_detik_articles()

    print("Total Articles:", total_articles)
    print("Detik Scraping Success:", detik_success)
    print("Detik Scraping Error:", detik_error)

    print("\n=== FILTER SUMMARY ===")

    print("Location Matches:", location_matches)
    print("Traffic Matches:", traffic_matches)
    print("Relevant Articles:", len(filtered_articles))

    print("\n=== RELEVANT ARTICLES ===")

    for item in filtered_articles:
        print("Title:", item["title"])
        print("Description:", item["description"])
        print("Location:", item["location_category"])
        print("Published At:", item["published_at"])
        print("Link:", item["link"])
        print("-" * 50)

    print("\n=== RSS DATA STRUCTURE TEST ===")

    print("Total Relevant Articles:", len(filtered_articles))

    if filtered_articles:
        first_article = filtered_articles[0]
        print("First Article:", first_article["title"])

    else:
        print("No relevant articles found.")

    print("\n=== STANDARDIZED DATA TEST ===")

    if filtered_articles:
        print("Source:", filtered_articles[0]["source"])
        print("Title:", filtered_articles[0]["title"])
        print("Description:", filtered_articles[0]["description"])
        print("Link:", filtered_articles[0]["link"])
        print("Published At:", filtered_articles[0]["published_at"])

    else:
        print("Belum ada artikel relevan untuk diperiksa")

    print("\n=== STANDARDIZED DATA SAMPLE TEST ===")

    sample_article = {
        "source": "Detik.com",
        "title": "Kemacetan terjadi di Tanjung Priok",
        "description": "Terjadi kemacetan di kawasan Tanjung Priok.",
        "link": "https://example.com/berita",
        "published_at": None,
        "location_category": "MAIN"
    }

    print("Source:", sample_article["source"])
    print("Title:", sample_article["title"])
    print("Description:", sample_article["description"])
    print("Link:", sample_article["link"])
    print("Published At:", sample_article["published_at"])
    print("Location:", sample_article["location_category"])