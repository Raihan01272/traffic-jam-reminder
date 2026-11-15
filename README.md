# Traffic Jam Reminder – Tanjung Priok

A Python-based traffic monitoring and notification system that collects traffic-related news from multiple sources, identifies incidents around Tanjung Priok, stores collected data in SQLite, generates Excel reports, and provides Telegram notifications.

## Project Overview

Traffic congestion and road incidents can affect daily commuting, especially in busy areas such as Tanjung Priok, North Jakarta.

This project aims to develop an automated traffic monitoring system using Python. It collects traffic-related information from multiple online news sources, processes and classifies articles based on their location and incident categories, and stores the results in a SQLite database.

The system also generates Excel reports and uses a Telegram Bot to provide traffic-related notifications.

### Project Objectives

- Collect traffic-related news from multiple sources.
- Identify news articles related to Tanjung Priok and nearby areas.
- Classify incidents such as brawls, demonstrations, and accidents involving traffic congestion.
- Store collected and processed data in an SQLite database.
- Generate structured traffic reports in Excel format.
- Provide Telegram notifications based on the monitoring results.

## Features

- **Multi-Source News Scraping**
  Collects traffic-related news from Detik.com, CNA Indonesia, and the official North Jakarta government website.

- **Location Classification**
  Classifies news articles into three location categories: `MAIN`, `NEARBY`, and `NOT_RELEVANT`.

- **Incident Classification**
  Identifies traffic-related incidents, including brawls, demonstrations, and accidents involving traffic congestion.

- **Data Validation and Deduplication**
  Validates collected articles and prevents duplicate records based on article links.

- **SQLite Database Integration**
  Stores validated news articles and their classification results in an SQLite database.

- **Excel Reporting**
  Generates structured Excel reports with summaries by news source, location, and incident category.

- **Telegram Notification System**
  Provides notification logic for traffic alerts and safe conditions. The main application currently uses dry-run mode for notification testing.

## Technologies Used

### Programming Language
- **Python** – Main programming language used to develop the monitoring pipeline.

### Libraries and Modules
- **Requests** – Sends HTTP requests to retrieve news data from online sources.
- **BeautifulSoup4** – Parses HTML content and extracts relevant text.
- **ElementTree** – Parses RSS feeds in XML format.
- **OpenPyXL** – Creates and formats Excel reports.
- **SQLite3** – Provides database connectivity and data storage.

### Tools and Services
- **SQLite** – Relational database for storing collected news articles.
- **Telegram Bot API** – Supports the notification system.
- **Git** – Tracks changes in the source code.
- **GitHub** – Hosts the project repository.

## Project Structure

```text
traffic-jam-reminder/
│
├── main.py
├── scraper.py
├── test_cna_rss.py
├── jakarta_utara_scraper.py
├── dummy_scraper.py
├── multi_source_scraper.py
│
├── database.py
├── notification_manager.py
├── telegram_notifier.py
├── export_to_excel.py
│
├── check_unique_index.py
├── test_duplicate.py
├── test_notification.py
│
├── run_traffic_reminder.bat
├── README.md
└── .gitignore
```

### File Descriptions

| File | Description |
|---|---|
| `main.py` | Main entry point that coordinates the monitoring pipeline. |
| `scraper.py` | Collects news articles from Detik.com. |
| `test_cna_rss.py` | Retrieves and parses news from CNA Indonesia RSS. |
| `jakarta_utara_scraper.py` | Collects news from the official North Jakarta government website. |
| `dummy_scraper.py` | Provides sample news data for testing. |
| `multi_source_scraper.py` | Combines news from multiple sources, validates articles, removes duplicates, and classifies locations and incidents. |
| `database.py` | Stores and retrieves collected news articles using SQLite. |
| `notification_manager.py` | Tracks previously sent articles to prevent repeated notifications. |
| `telegram_notifier.py` | Handles Telegram notification logic. |
| `export_to_excel.py` | Generates Excel reports from stored news data. |
| `check_unique_index.py` | Checks database indexes for diagnostic purposes. |
| `test_duplicate.py` | Tests duplicate prevention in the database. |
| `test_notification.py` | Tests Telegram notification scenarios using dry-run mode. |
| `run_traffic_reminder.bat` | Runs the main application using the project's Python virtual environment. |
| `.gitignore` | Excludes local files, credentials, and generated files from Git tracking. |

## Installation and Setup

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Raihan01272/traffic-jam-reminder.git
```

Navigate to the project directory:

```bash
cd traffic-jam-reminder
```

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install requests beautifulsoup4 openpyxl python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your own Telegram Bot credentials:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Do not share or commit the `.env` file to GitHub.

### 5. Run the Application

Run the main application:

```bash
python main.py
```

**

## Install Dependencies

Install all required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## How to Use

After completing the installation and configuration steps, follow these instructions to run the Traffic Jam Reminder application.

### 1. Run the Application

Activate the virtual environment and execute:

```bash
python main.py
```

The application will start the multi-source traffic monitoring pipeline.

### 2. News Collection

The application collects news articles from the following sources:

- Detik.com
- CNA Indonesia
- Official North Jakarta Government Website

Dummy News is also available for testing purposes and is not treated as a real news source.

### 3. Data Processing

Collected articles go through several processing steps:

- **Data Validation:** Checks whether the collected articles contain the required information.
- **Location Classification:** Categorizes articles as `MAIN`, `NEARBY`, or `NOT_RELEVANT`.
- **Incident Classification:** Identifies incidents such as brawls, demonstrations, and accidents involving traffic congestion.
- **Deduplication:** Prevents duplicate articles from being processed repeatedly.

### 4. Database Storage

Validated articles are stored in the SQLite database:

```text
traffic_jam.db
```

The database keeps article information and supports the notification tracking process.

### 5. Excel Report Generation

The application generates an Excel report:

```text
traffic_report.xlsx
```

The report contains collected traffic news and summary information.

### 6. Telegram Notifications

The application includes notification logic for two conditions:

- **Traffic Alert:** Notifies users when qualifying traffic incidents are detected in the main monitoring area.
- **Safe Condition:** Sends a predefined message when no qualifying traffic alerts are found.

The current main application uses `dry_run=True`, so notifications are simulated and are not sent as actual Telegram messages.

## Example Output

The following examples illustrate the expected output of the Traffic Jam Reminder application.

### 1. News Scraping Output

The application collects news articles from multiple sources.

```text
=== MULTI-SOURCE NEWS SCRAPING ===

Source: Detik.com
Source: CNA Indonesia
Source: Jakarta Utara Government Website

Total articles collected: [number]
```

### 2. Location Classification

Each collected article is classified based on its location.

| Location | Description |
|---|---|
| `MAIN` | Articles related to Tanjung Priok. |
| `NEARBY` | Articles related to surrounding areas in North Jakarta. |
| `NOT_RELEVANT` | Articles outside the monitoring area. |

### 3. Incident Classification

The application identifies selected traffic-related incidents, including:

- `TAWURAN`
- `DEMO`
- `KECELAKAAN_DAN_MACET`

Only articles that meet the configured location and incident criteria are considered for traffic alerts.

### 4. Generated Excel Report

The application generates an Excel file named:

```text
traffic_report.xlsx
```

The report contains article data and summary information to help review the collected news.

### 5. Notification Simulation

Example of the notification logic in dry-run mode:

```text
=== TELEGRAM NOTIFICATION (DRY RUN) ===

macet bang, cari alternatif lain jalannya biar ga telat ngantor
```

The message above is displayed as a simulation and is not sent to Telegram while dry-run mode is enabled.

## Limitations

The current version of Traffic Jam Reminder has several limitations:

- **News-Based Monitoring:** The system relies on online news articles rather than direct traffic data from GPS, CCTV, or road sensors.
- **Source Availability:** Data collection depends on the availability and structure of external news websites.
- **Keyword-Based Classification:** Location and incident classification relies on predefined keywords, which may produce false positives or false negatives.
- **Geographical Coverage:** The monitoring area focuses on Tanjung Priok and selected surrounding areas in North Jakarta.
- **Notification Testing:** Telegram notifications currently operate in dry-run mode in the main application.

## Future Improvements

Potential improvements for future development include:

- Integrating additional news sources.
- Improving location and incident classification using Natural Language Processing (NLP).
- Integrating traffic data APIs where available.
- Developing an interactive dashboard for traffic monitoring and data visualization.
- Enabling reliable automated Telegram notifications.
- Expanding geographical coverage to other areas of Jakarta.
- Improving automated testing and error handling.

## Project Status

**Status: In Development**

Traffic Jam Reminder is an ongoing Python project focused on monitoring traffic-related news around Tanjung Priok, North Jakarta.

The current version supports multi-source news collection, location and incident classification, SQLite database storage, Excel report generation, and Telegram notification simulation.

Further improvements are planned to enhance classification accuracy, source reliability, and notification automation.