import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


url = "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml"


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    description = soup.get_text(
        separator=" ",
        strip=True
    )

    return description


def fetch_cna_articles():

    cna_articles = []

    response = None
    error_message = None
    cna_success = False

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        channel = root.find("channel")

        if channel is None:
            raise ValueError("Channel RSS tidak ditemukan")

        articles = channel.findall("item")

        for article in articles:

            title = article.findtext(
                "title",
                default=""
            ).strip()

            link = article.findtext(
                "link",
                default=""
            ).strip()

            raw_description = article.findtext(
                "description",
                default=""
            )

            description = clean_html(raw_description)

            raw_published_at = article.findtext(
                "pubDate",
                default=""
            ).strip()

            try:
                published_at = parsedate_to_datetime(
                    raw_published_at
                )
            except (TypeError, ValueError):
                published_at = None

            article_data = {
                "source": "CNA Indonesia",
                "title": title,
                "description": description,
                "link": link,
                "published_at": published_at
            }

            cna_articles.append(article_data)

        cna_success = True

    except requests.exceptions.RequestException as error:
        error_message = f"Request Error: {error}"

    except ET.ParseError as error:
        error_message = f"XML Parsing Error: {error}"

    except ValueError as error:
        error_message = str(error)

    return (
        cna_articles,
        response,
        error_message,
        cna_success
    )


if __name__ == "__main__":

    cna_articles, response, error_message, cna_success = fetch_cna_articles()

    print("CNA Scraping Success:", cna_success)
    print("CNA Scraping Error:", error_message)

    print("\n=== CNA RSS TEST ===")

    if error_message:
        print("Error:", error_message)

    elif response is not None:
        print("HTTP Status:", response.status_code)
        print("Content Type:", response.headers.get("Content-Type"))

    print("Total CNA Articles:", len(cna_articles))

    for article in cna_articles[:5]:

        print("\nTitle:", article["title"])
        print("Link:", article["link"])
        print("Description:", article["description"])
        print("Published At:", article["published_at"])
        print("-" * 50)

    print("\n=== STANDARDIZED DATA TEST ===")

    print("Total Standardized Articles:", len(cna_articles))

    if cna_articles:
        print("\nFirst Article:")
        print(cna_articles[0])

        print("\n=== PUBLISHED DATE TYPE TEST ===")

        print(
            "Tanggal:",
            cna_articles[0]["published_at"]
        )

        print(
            "Tipe:",
            type(cna_articles[0]["published_at"])
        )