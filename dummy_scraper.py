from pathlib import Path
from bs4 import BeautifulSoup

# 1. Menentukan lokasi file HTML
html_path = Path(__file__).parent / "dummy_news.html"

# 2. Membuka dan membaca file HTML
with open(html_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# 3. Membaca struktur HTML menggunakan BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# 4. Mengambil semua elemen artikel
articles = soup.find_all("div", class_="article")

# 5. Menampilkan hasil
dummy_articles = []

for article in articles:
    title = article.find("h2", class_="title")
    description = article.find("p", class_="description")
    link = article.find("a", class_="link")

    article_data = {
        "source": "Dummy News",
        "title": title.get_text(strip=True) if title else "",
        "description": description.get_text(strip=True) if description else "",
        "link": link.get("href", "") if link else ""
    }

    dummy_articles.append(article_data)


# 6. Menampilkan hasil

print("=== DUMMY NEWS SCRAPER ===")
print("Total Articles:", len(dummy_articles))

for article in dummy_articles:
    print("\nSource:", article["source"])
    print("Title:", article["title"])
    print("Description:", article["description"])
    print("Link:", article["link"])
    print("-" * 50)