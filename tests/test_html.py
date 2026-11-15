from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <div class="article">
            <h2>traffic congestion at Yos Sudarso Street</h2>
            <p class="location">Yos Sudarso Street</p>
        </div>

        <div class="article">
            <h2>traffic congestion at Tanjung Priok Port</h2>
            <p class="location">Tanjung Priok Port</p>    
        </div>

        <div class="article">
            <h2>traffic vehicle queue on Enggano Street</h2>
            <p class="location">Enggano Street</p>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all("div", class_="article")

for article in articles:
    title = article.find("h2").get_text(strip=True)
    location = article.find("p", class_="location").get_text(strip=True)
   
    print("Title:", title)
    print("Location:", location)
    print("--------------------")