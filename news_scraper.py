// Thanks ChatGPT

import requests

SERPAPI_KEY = "your_serpapi_key"

params = {
    "engine": "google_news",
    "q": "top news",  # Query for top news
    "hl": "en",       # Language (English)
    "gl": "us",       # Country (United States)
    "num": 1,         # Get only the top 1 news story
    "api_key": SERPAPI_KEY
}

response = requests.get("https://serpapi.com/search", params=params)
news_data = response.json()

# Extract the first news result
if "news_results" in news_data:
    top_news = news_data["news_results"][0]  # First news story
    title = top_news["title"]
    link = top_news["link"]
    source = top_news["source"]
    published = top_news["date"]

    print(f"Title: {title}")
    print(f"Source: {source}")
    print(f"Published: {published}")
    print(f"Link: {link}")
else:
    print("No news results found.")
