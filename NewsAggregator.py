import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Define accepted sources (must match exact spelling in API response)
ACCEPTED_SOURCES = {"The Associated Press", "Reuters", "BBC.com"}

# Google Sheets Setup
SHEET_NAME = "News_Aggregator"  # Change to your Google Sheet name
CREDENTIALS_FILE = "config/credentials.json"  # Path to your downloaded JSON file

def authenticate_google_sheets():
    """Authenticate and return the Google Sheets client."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def append_to_google_sheets(news_data):
    """Append news stories to Google Sheets."""
    client = authenticate_google_sheets()
    sheet = client.open(SHEET_NAME).sheet1  # Select first worksheet

    # Add header if the sheet is empty
    if not sheet.get_all_values():
        sheet.append_row(["Timestamp", "Source", "Category", "Title", "Link"])

    # Append each news story
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for source, categories in news_data.items():
        for category, story in categories.items():
            if story:
                sheet.append_row([timestamp, source, category, story["title"], story["link"]])

def get_news_by_source(api_key, query, date):
    """Fetch and return the top story per source for AP, Reuters, and BBC.com."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "tbs": f"cdr:1,cd_min:{date},cd_max:{date}",  # Filter by date
        "hl": "en",
        "gl": "us",
        "num": 20  # Fetch more stories to increase chances of getting desired sources
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Ensure 'news_results' exists in response
    if "news_results" not in data:
        print("Error: 'news_results' key not found in the response.")
        return {source: None for source in ACCEPTED_SOURCES}

    # Dictionary to store one story per source
    news_by_source = {source: None for source in ACCEPTED_SOURCES}

    for article in data["news_results"]:
        source_name = article.get("source", {}).get("name", "")
        if source_name in ACCEPTED_SOURCES and news_by_source[source_name] is None:
            news_by_source[source_name] = {"title": article["title"], "link": article["link"]}

        # Stop when we have collected one story per source
        if all(news_by_source.values()):
            break

    return news_by_source

def main():
    # Ask for user input
    api_key = input("Enter your SerpAPI Key: ").strip()
    date = input("Enter the date (YYYY-MM-DD) for the news: ").strip()

    if not api_key:
        print("API Key is required. Exiting...")
        return

    try:
        # Fetch US news and world news
        us_news = get_news_by_source(api_key, "top news in the US", date)
        world_news = get_news_by_source(api_key, "world news", date)

        # Organize data for Google Sheets
        news_data = {}
        for source in ACCEPTED_SOURCES:
            news_data[source] = {
                "US": us_news.get(source),
                "World": world_news.get(source)
            }

        # Append data to Google Sheets
        append_to_google_sheets(news_data)

        # Output results
        print("\nTop US News Stories (One per Source):")
        for source in ACCEPTED_SOURCES:
            story = us_news.get(source)
            print(f"{source}: {story['title']} ({story['link']})" if story else f"{source}: No story found.")

        print("\nTop World News Stories (One per Source):")
        for source in ACCEPTED_SOURCES:
            story = world_news.get(source)
            print(f"{source}: {story['title']} ({story['link']})" if story else f"{source}: No story found.")

        print("\nNews successfully added to Google Sheets!")

    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    main()
