from multi_source_scraper import classify_incident

test_cases = [
    "Banjir menyebabkan jalan Tanjung Priok terendam dan lalu lintas terganggu",
    "Jalan ditutup akibat pohon tumbang di Tanjung Priok",
    "Camat Tanjung Priok pantau titik genangan",
    "Banjir melanda permukiman Tanjung Priok"
]

for text in test_cases:
    print("Text:", text)
    print("Incident:", classify_incident(text))
    print("-" * 50)