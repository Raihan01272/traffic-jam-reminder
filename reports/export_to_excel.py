import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def export_to_excel():

    connection = sqlite3.connect("traffic_jam.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            source,
            title,
            location_category,
            incident_category,
            link,
            scraped_at
        FROM news_articles
        ORDER BY id ASC
    """)

    articles = cursor.fetchall()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Traffic Report"

    headers = [
        "ID",
        "Source",
        "Title",
        "Location",
        "Incident",
        "Link",
        "Scraped At"
    ]

    worksheet.append(headers)

    for article in articles:
        worksheet.append(article)

    # Formatting header
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )
        cell.alignment = Alignment(horizontal="center")

    column_widths = {
        "A": 8,
        "B": 20,
        "C": 55,
        "D": 20,
        "E": 30,
        "F": 60,
        "G": 22
    }

    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    summary = workbook.create_sheet("Summary")

    summary["A1"] = "TRAFFIC JAM REMINDER REPORT"
    summary["A3"] = "Total Articles"
    summary["B3"] = len(articles)

    summary["A5"] = "ARTICLES BY SOURCE"

    cursor.execute("""
        SELECT source, COUNT(*)
        FROM news_articles
        GROUP BY source
    """)

    source_data = cursor.fetchall()

    summary["A6"] = "Source"
    summary["B6"] = "Total"

    row = 7

    for source, total in source_data:
        summary.cell(row=row, column=1, value=source)
        summary.cell(row=row, column=2, value=total)
        row += 1

    summary["D5"] = "ARTICLES BY LOCATION"

    cursor.execute("""
        SELECT location_category, COUNT(*)
        FROM news_articles
        GROUP BY location_category
    """)

    location_data = cursor.fetchall()

    summary["D6"] = "Location"
    summary["E6"] = "Total"

    row = 7

    for location, total in location_data:
        summary.cell(row=row, column=4, value=location)
        summary.cell(row=row, column=5, value=total)
        row += 1

    summary["G5"] = "ARTICLES BY INCIDENT"

    cursor.execute("""
        SELECT incident_category, COUNT(*)
        FROM news_articles
        GROUP BY incident_category
    """)

    incident_data = cursor.fetchall()

    summary["G6"] = "Incident"
    summary["H6"] = "Total"

    row = 7

    for incident, total in incident_data:
        summary.cell(row=row, column=7, value=incident)
        summary.cell(row=row, column=8, value=total)
        row += 1

    # Mengatur lebar kolom Summary
    for column in ["A", "D", "G"]:
        summary.column_dimensions[column].width = 30

    for column in ["B", "E", "H"]:
        summary.column_dimensions[column].width = 15

    workbook.save("traffic_report.xlsx")

    connection.close()

    print("\n=== EXCEL REPORT ===")
    print("Total artikel:", len(articles))
    print("Formatting berhasil diterapkan!")
    print("File: traffic_report.xlsx")

    return len(articles)

if __name__ == "__main__":
    print("Export Excel module berhasil dijalankan.")