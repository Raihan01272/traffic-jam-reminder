import re

keyword = "padat"

test_cases = [
    "Kemacetan selama 2 jam"
    "Saya makan jamur"
    "Jalanan macet parah"
    "Jam malam dimulai pukul 10"
]

for text in test_cases:
    
    result = re.search(
        r"\b" + re.escape(keyword) + r"\b",
        text.lower()
    )

    print(text, "=>", result is not None)