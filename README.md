# Traffic Jam Reminder – Tanjung Priok

A Python-based traffic monitoring and notification system that collects news articles from multiple sources, identifies traffic-related incidents around Tanjung Priok, and generates reports with optional Telegram notifications.

## Overview

Traffic Jam Reminder is a data engineering project designed to monitor news related to traffic incidents in Tanjung Priok, North Jakarta.

The application collects news from multiple sources, validates and removes duplicate articles, classifies locations and incidents, stores the results in SQLite, and exports reports to Excel.

The system can also simulate or send Telegram notifications based on detected incidents.

## Features

- Multi-source news scraping using RSS and web scraping.
- Location classification:
  - MAIN: Tanjung Priok.
  - NEARBY: surrounding areas.
  - NOT_RELEVANT: unrelated locations.
- Incident classification:
  - TAWURAN
  - DEMO
  - KECELAKAAN_DAN_MACET
- Article validation and duplicate detection.
- SQLite database storage.
- Excel report generation.
- Telegram notification with dry-run support.
- Scheduled execution using Windows Task Scheduler.
- Dummy news data for testing.

## Technologies

- Python
- Requests
- BeautifulSoup
- SQLite
- OpenPyXL
- Python-dotenv
- XML / RSS
- Telegram Bot API
- Git and GitHub

## Project Structure

```text
traffic-jam-reminder/
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── notifications/
│   ├── __init__.py
│   ├── notification_manager.py
│   └── telegram_notifier.py
│
├── reports/
│   ├── __init__.py
│   └── export_to_excel.py
│
├── scrapers/
│   ├── __init__.py
│   ├── scraper.py
│   ├── test_cna_rss.py
│   ├── dummy_scraper.py
│   └── jakarta_utara_scraper.py
│
├── scripts/
│   ├── __init__.py
│   ├── check_database.py
│   ├── check_notification_table.py
│   ├── check_unique_index.py
│   ├── cleanup_test.py
│   ├── create_excel.py
│   ├── create_notification_table.py
│   └── fix_notification_table.py
│
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   └── dummy_news.html
│   ├── test_duplicate.py
│   ├── test_html.py
│   ├── test_notification.py
│   ├── test_real_rss.py
│   ├── test_regex.py
│   ├── test_requests.py
│   └── test_rss.py
│
├── main.py
├── multi_source_scraper.py
├── requirements.txt
├── run_traffic_reminder.bat
├── .env.example
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Raihan01272/traffic-jam-reminder.git
cd traffic-jam-reminder
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Example:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Never upload your actual `.env` file or Telegram credentials to GitHub.

## Usage

Run the application:

```powershell
python main.py
```

The application will:

1. Collect articles from configured news sources.
2. Validate article data.
3. Remove duplicate URLs.
4. Classify locations and incidents.
5. Store real news articles in SQLite.
6. Generate an Excel report.
7. Process eligible Telegram notifications.

Telegram notifications are configured with dry-run mode in the main application.

## Reports and Database

The application uses SQLite to store collected articles and notification history.

Excel reports are generated as:

```text
traffic_report.xlsx
```

The database and generated reports are local runtime files and are not included in the repository.

## Scheduled Execution

The project includes:

```text
run_traffic_reminder.bat
```

This batch file can be configured with Windows Task Scheduler to run the application automatically.

## Safety and Limitations

- News scraping depends on the availability and structure of external sources.
- News classification depends on predefined keywords.
- A location mentioned in an article does not always mean that a traffic incident is occurring there.
- Notifications are suppressed if a configured real news source fails.
- Dummy News is intended for testing and must not be treated as real news.
- Telegram dry-run mode prevents actual message delivery.

## Project Status

Core scraping, classification, validation, SQLite storage, Excel reporting, Telegram notification logic, and scheduled execution have been implemented.

The project is undergoing final testing and documentation improvements.

## Author

Muhammad Raihan

GitHub: [Raihan01272](https://github.com/Raihan01272)
