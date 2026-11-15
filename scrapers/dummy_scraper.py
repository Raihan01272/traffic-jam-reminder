from pathlib import Path
from bs4 import BeautifulSoup


def fetch_dummy_articles():

    html_path = (
        Path(__file__).resolve().parents[1]
        / "tests"
        / "fixtures"
        / "dummy_news.html"
    )

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    article_elements = soup.find_all("div", class_="article")

    articles = []

    for article in article_elements:

        title = article.find("h2", class_="title").get_text(strip=True)

        description = article.find("p", class_="description").get_text(strip=True)

        link = article.find("a", class_="link")["href"]

        text = title + " " + description

        if "tanjung priok" in text.lower() or "priok" in text.lower():
            location_category = "MAIN"
        else:
            location_category = "NEARBY"

        dummy_article = {
            "source": "Dummy News",
            "title": title,
            "description": description,
            "link": link,
            "location_category": location_category
        }

        articles.append(dummy_article)

    return articles
