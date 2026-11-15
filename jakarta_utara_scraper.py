import requests
from bs4 import BeautifulSoup

JAKARTA_UTARA_URL = (
    "https://utara.jakarta.go.id/"
    "kecamatan/tanjung-priok/publikasi?tab=berita"
)


def test_jakarta_utara_connection():
    print("Menghubungkan ke website Jakarta Utara...")

    try:
        response = requests.get(
            JAKARTA_UTARA_URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print("HTTP Status:", response.status_code)

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        print("Page Title:", soup.title.get_text(strip=True))

        article_links = soup.find_all(
            "a",
            href=True
        )

        print("Total tautan ditemukan:", len(article_links))

        print("\n=== CONTOH TAUTAN BERITA ===")

        for link in article_links:
            href = link["href"]
            title = link.get_text(" ", strip=True)

            if "/berita/" in href and title:
                print("Judul:", title[:150])
                print("Link:", href)
                print("-" * 50)

    except requests.exceptions.RequestException as error:
        print("Terjadi kesalahan koneksi:", error)



def test_article_detail(article_url):
    print("\n=== TEST ARTICLE DETAIL ===")

    try:
        response = requests.get(
            article_url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.find("h1")

        description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        print(
            "Judul:",
            title.get_text(" ", strip=True) if title else "Tidak ditemukan"
        )

        print(
            "Deskripsi:",
            description.get("content") if description else "Tidak ditemukan"
        )

        print("HTTP Status:", response.status_code)

    except requests.exceptions.RequestException as error:
        print("Gagal mengambil detail artikel:", error)



def fetch_jakarta_utara_articles():
    articles = []

    print("\n=== FETCH JAKARTA UTARA ARTICLES ===")

    try:
        response = requests.get(
            JAKARTA_UTARA_URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        article_links = soup.find_all("a", href=True)

        for item in article_links:
            href = item["href"]
            title = item.get_text(" ", strip=True)

            if "/berita/" not in href:
                continue

            if not title:
                continue

            if href.startswith("/"):
                article_url = "https://utara.jakarta.go.id" + href
            else:
                article_url = href

            try:
                article_response = requests.get(
                    article_url,
                    timeout=30,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                article_response.raise_for_status()

                article_soup = BeautifulSoup(
                    article_response.text,
                    "html.parser"
                )

                heading = article_soup.find("h1")

                description_tag = article_soup.find(
                    "meta",
                    attrs={"name": "description"}
                )

                if not heading:
                    continue

                article_title = heading.get_text(
                    " ",
                    strip=True
                )

                description = ""

                if description_tag:
                    description = description_tag.get("content", "")

                articles.append({
                    "source": "Jakarta Utara",
                    "title": article_title,
                    "description": description,
                    "link": article_url
                })

            except requests.exceptions.RequestException as error:
                print("Gagal mengambil artikel:", article_url)
                print("Error:", error)

        print("Total artikel berhasil diambil:", len(articles))

        return articles, True, None

    except requests.exceptions.RequestException as error:
        print("Gagal mengambil halaman publikasi:", error)
        return [], False, str(error)



if __name__ == "__main__":

    (
        jakarta_utara_articles,
        jakarta_utara_success,
        jakarta_utara_error
    ) = fetch_jakarta_utara_articles()

    print("\n=== JAKARTA UTARA SOURCE HEALTH ===")
    print("Success:", jakarta_utara_success)
    print("Error:", jakarta_utara_error)

    print("\n=== JAKARTA UTARA ARTICLE RESULT ===")
    print("Total Articles:", len(jakarta_utara_articles))

    for article in jakarta_utara_articles:

        print("\nTitle:", article["title"])
        print("Description:", article["description"])
        print("Link:", article["link"])
        print("-" * 50)