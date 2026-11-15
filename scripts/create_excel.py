from openpyxl import Workbook
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

workbook = Workbook()

worksheet = workbook.active

workbook.title = "Traffic Report"

worksheet.append([
    "ID",
    "Source",
    "Title",
    "Location",
    "Incident",
    "Link",
    "Scraped At"
])

workbook.save(PROJECT_ROOT / "traffic_report.xlsx")

print("File Excel berhasil dibuat")