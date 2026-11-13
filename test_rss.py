import xml.etree.ElementTree as ET

rss_data = """
<rss>
    <channel>
        <title>Tanjung Priok Newspaper</title>
        
        <item>
            <title>congestion in Tanjung Priok</title>
            <pubDate>04 November 2026</pubDate>
            <link>https://www.example.com/congestion-in-tanjung-priok</link>
        </item>

        <item>
            <title>queue in Tanjung Priok</title>
            <pubDate>05 November 2026</pubDate>
            <link>https://www.example.com/queue-in-tanjung-priok</link>
        </item>
        
        <item>
            <title>traffic jam in Tanjung Priok</title>
            <pubDate>06 November 2026</pubDate>
            <link>https://www.example.com/traffic-jam-in-tanjung-priok</link>
        </item>
    </channel>
</rss>
"""

root = ET.fromstring(rss_data)

channel = root.find("channel")

articles = channel.findall("item")

for article in articles:

    title = article.findtext("title")
    date = article.findtext("pubDate")
    link = article.findtext("link")

print("Title:", title)
print("Date:", date)
print("Link:", link)
print("------------------")