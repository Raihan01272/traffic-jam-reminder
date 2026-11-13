import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

url = "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml"

cna_articles = []

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    channel = root.find("channel")

    if channel is None:
        print("Channel RSS tidak ditemukan")

    else:
        articles = channel.findall("item")

        for article in articles:
            title = article.findtext("title", default="")
            link = article.findtext("link", default="")
            raw_description = article.findtext(
                "description",
                default=""
            )

            soup = BeautifulSoup(raw_description, "html.parser")
            description = soup.get_text(
                separator=" ",
                strip=True
            )

            article_data = {
                "source": "CNA Indonesia",
                "title": title,
                "description": description,
                "link": link
            }

            cna_articles.append(article_data)

except requests.exceptions.RequestException as error:
    print("Request Error:", error)

except ET.ParseError as error:
    print("XML Parsing Error:", error)


# Bagian pengujian hanya berjalan jika file dijalankan langsung
if __name__ == "__main__":
    print("=== CNA RSS TEST ===")
    print("HTTP Status:", response.status_code)
    print("Content Type:", response.headers.get("Content-Type"))
    print("Total CNA Articles:", len(cna_articles))

    for article in cna_articles[:5]:
        print("\nTitle:", article["title"])
        print("Link:", article["link"])
        print("Description:", article["description"])
        print("-" * 50)

    print("\n=== STANDARDIZED DATA TEST ===")
    print("Total Standardized Articles:", len(cna_articles))

    if cna_articles:
        print("\nFirst Article:")
        print(cna_articles[0])
