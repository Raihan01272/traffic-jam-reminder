import requests
from bs4 import BeautifulSoup

url = "https://www.example.com"

response = requests.get(url, timeout=15)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.get_text(strip=True)

print("Website Title:", title)

paragraphs = soup.find_all("p")

for paragraph in paragraphs:
    print("Paragraph:", paragraph.get_text(strip=True))