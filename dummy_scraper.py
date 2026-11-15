from pathlib import Path
from bs4 import BeautifulSoup


def fetch_dummy_articles():

    html_path = Path(__file__).parent / "dummy_news.html"

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    articles = soup.find_all("div", class_="article")

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

    return dummy_articles

if __name__ == "__main__":

    dummy_articles = fetch_dummy_articles()

    print("=== DUMMY NEWS SCRAPER ===")
    print("Total Articles:", len(dummy_articles))

    for article in dummy_articles:

        print("\nSource:", article["source"])
        print("Title:", article["title"])
        print("Description:", article["description"])
        print("Link:", article["link"])
        print("-" * 50)