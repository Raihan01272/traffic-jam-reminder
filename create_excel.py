from openpyxl import Workbook

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

workbook.save("traffic_report.xlsx")

print("File Excel berhasil dibuat")