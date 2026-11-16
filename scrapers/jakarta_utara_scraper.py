import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urljoin


JAKARTA_UTARA_URL = (
    "https://utara.jakarta.go.id/"
    "kecamatan/tanjung-priok/publikasi?tab=berita"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TIMEOUT = 30


def parse_published_date(raw_date):
    """
    Mengubah teks tanggal menjadi objek datetime.
    Mengembalikan None jika tanggal tidak dapat dibaca.
    """

    if not raw_date:
        return None

    raw_date = str(raw_date).strip()

    try:
        return parsedate_to_datetime(raw_date)
    except (TypeError, ValueError, OverflowError):
        pass

    try:
        return datetime.fromisoformat(
            raw_date.replace("Z", "+00:00")
        )
    except (TypeError, ValueError):
        pass

    return None


def extract_published_date(soup):
    """
    Mencari tanggal publikasi dari beberapa sumber
    yang mungkin tersedia di HTML artikel.
    """

    date_selectors = [
        {"property": "article:published_time"},
        {"name": "date"},
        {"name": "publishdate"},
        {"name": "pubdate"},
        {"itemprop": "datePublished"},
        {"property": "og:updated_time"},
    ]

    for attributes in date_selectors:
        element = soup.find("meta", attrs=attributes)

        if element:
            raw_date = element.get("content")
            published_at = parse_published_date(raw_date)

            if published_at:
                return published_at

    time_elements = soup.find_all("time")

    for element in time_elements:
        raw_date = (
            element.get("datetime")
            or element.get_text(" ", strip=True)
        )

        published_at = parse_published_date(raw_date)

        if published_at:
            return published_at

    json_ld_elements = soup.find_all(
        "script",
        attrs={"type": "application/ld+json"}
    )

    for element in json_ld_elements:
        try:
            data = json.loads(element.string or element.get_text())
        except (json.JSONDecodeError, TypeError):
            continue

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            continue

        for item in data:
            if not isinstance(item, dict):
                continue

            raw_date = (
                item.get("datePublished")
                or item.get("dateCreated")
            )

            published_at = parse_published_date(raw_date)

            if published_at:
                return published_at

            graph = item.get("@graph", [])

            if isinstance(graph, list):
                for graph_item in graph:
                    if not isinstance(graph_item, dict):
                        continue

                    raw_date = (
                        graph_item.get("datePublished")
                        or graph_item.get("dateCreated")
                    )

                    published_at = parse_published_date(
                        raw_date
                    )

                    if published_at:
                        return published_at

    return None


def test_jakarta_utara_connection():

    print("\n=== TEST KONEKSI JAKARTA UTARA ===")

    try:
        response = requests.get(
            JAKARTA_UTARA_URL,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        article_links = soup.find_all(
            "a",
            href=re.compile(r"/berita/")
        )

        print("Status:", response.status_code)
        print("Jumlah link berita:", len(article_links))

        return True

    except requests.RequestException as error:
        print("Koneksi gagal:", error)
        return False


def test_article_detail(article_url):

    print("\n=== TEST ARTICLE DETAIL ===")

    try:
        response = requests.get(
            article_url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.find("h1")

        meta_description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        content_area = soup.select_one(
            ".article-content"
        )

        published_at = extract_published_date(soup)

        print("\n=== JUDUL ARTIKEL ===")

        if title:
            print(title.get_text(" ", strip=True))
        else:
            print("Judul tidak ditemukan.")

        print("\n=== META DESCRIPTION ===")

        if meta_description:
            print(meta_description.get("content"))
        else:
            print("Meta description tidak ditemukan.")

        print("\n=== PEMERIKSAAN METADATA TANGGAL ===")

        date_selectors = [
            {"property": "article:published_time"},
            {"name": "date"},
            {"name": "publishdate"},
            {"name": "pubdate"},
            {"itemprop": "datePublished"},
            {"property": "og:updated_time"},
        ]

        for attributes in date_selectors:
            element = soup.find(
                "meta",
                attrs=attributes
            )

            if element:
                print(
                    attributes,
                    ":",
                    element.get("content")
                )

        print("\n=== ELEMEN TIME ===")

        time_elements = soup.find_all("time")

        if time_elements:
            for element in time_elements:
                print(
                    "Text:",
                    element.get_text(" ", strip=True)
                )

                print(
                    "Datetime:",
                    element.get("datetime")
                )
        else:
            print("Tag <time> tidak ditemukan.")

        print("\n=== HASIL TANGGAL PUBLIKASI ===")

        print("Tanggal:", published_at)
        print("Tipe:", type(published_at))

        if published_at is None:
            print(
                "PERINGATAN: Tanggal publikasi "
                "belum berhasil ditemukan."
            )

        print("\n=== PEMERIKSAAN STRUKTUR ARTIKEL ===")

        print(
            "Tag <article> ditemukan:",
            "Ya" if soup.find("article") else "Tidak"
        )

        print(
            "Tag <main> ditemukan:",
            "Ya" if soup.find("main") else "Tidak"
        )

        print(
            "Class .article-content ditemukan:",
            "Ya" if content_area else "Tidak"
        )

        print("\n=== INFORMASI TAMBAHAN ===")

        print("HTTP Status:", response.status_code)
        print("Panjang HTML:", len(response.text), "karakter")

        return published_at

    except requests.RequestException as error:
        print("Gagal mengambil detail artikel:", error)
        return None


def fetch_jakarta_utara_articles():

    articles = []

    try:
        response = requests.get(
            JAKARTA_UTARA_URL,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        article_links = soup.find_all(
            "a",
            href=re.compile(r"/berita/")
        )

        unique_links = []

        for link in article_links:

            href = link.get("href")

            if not href:
                continue

            article_url = urljoin(
                JAKARTA_UTARA_URL,
                href
            )

            if article_url not in unique_links:
                unique_links.append(article_url)

        unique_links = unique_links[:12]

        print(
            "\nTotal link artikel:",
            len(unique_links)
        )

        for article_url in unique_links:

            try:
                article_response = requests.get(
                    article_url,
                    headers=HEADERS,
                    timeout=TIMEOUT
                )

                article_response.raise_for_status()

                article_soup = BeautifulSoup(
                    article_response.text,
                    "html.parser"
                )

                title_tag = article_soup.find("h1")

                if title_tag:
                    article_title = title_tag.get_text(
                        " ",
                        strip=True
                    )
                else:
                    article_title = ""

                content_area = article_soup.select_one(
                    ".article-content"
                )

                if content_area:
                    paragraphs = content_area.find_all("p")

                    article_description = " ".join(
                        paragraph.get_text(" ", strip=True)
                        for paragraph in paragraphs
                    )
                else:
                    meta_description = article_soup.find(
                        "meta",
                        attrs={"name": "description"}
                    )

                    if meta_description:
                        article_description = (
                            meta_description.get("content", "")
                        )
                    else:
                        article_description = ""

                published_at = extract_published_date(
                    article_soup
                )

                article = {
                    "source": "Jakarta Utara",
                    "title": article_title,
                    "description": article_description,
                    "link": article_url,
                    "published_at": published_at,
                }

                articles.append(article)

                print("\nArtikel berhasil diambil:")
                print("Judul:", article_title)
                print("Tanggal:", published_at)

            except requests.RequestException as error:
                print(
                    "Gagal mengambil artikel:",
                    article_url,
                    error
                )

        return articles, True, None

    except requests.RequestException as error:

        return [], False, str(error)


if __name__ == "__main__":

    print("=== JAKARTA UTARA SCRAPER ===")

    connection_success = test_jakarta_utara_connection()

    if connection_success:

        articles, success, error = (
            fetch_jakarta_utara_articles()
        )

        print("\n=== HASIL SCRAPING ===")

        print("Berhasil:", success)
        print("Jumlah artikel:", len(articles))

        if error:
            print("Error:", error)

        for index, article in enumerate(
            articles,
            start=1
        ):

            print("\nArtikel:", index)
            print("Sumber:", article["source"])
            print("Judul:", article["title"])
            print("Tanggal:", article["published_at"])
            print("Tipe tanggal:", type(article["published_at"]))
            print("Link:", article["link"])

        if articles:
            test_article_detail(
                articles[0]["link"]
            )