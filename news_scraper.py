import requests

# Define accepted sources (must match exact spelling in API response)
ACCEPTED_SOURCES = {"The Associated Press", "Reuters", "BBC.com"}

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

    # Print the raw response data for debugging (you can remove this line later)
    # print("Raw API Response:", data)

    # Ensure 'news_results' exists in response
    if "news_results" not in data:
        print("Error: 'news_results' key not found in the response.")
        return {}

    # Dictionary to store one story per source
    news_by_source = {source: None for source in ACCEPTED_SOURCES}

    for article in data["news_results"]:
        source_name = article.get("source", {}).get("name", "")

        # Ensure we only process articles from desired sources
        if source_name in ACCEPTED_SOURCES and news_by_source[source_name] is None:
            news_by_source[source_name] = f"{article['title']} - {source_name} ({article['link']})"

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

        # Output results
        print("\nTop US News Stories (One per Source):")
        for source in ACCEPTED_SOURCES:
            print(f"{source}: {us_news.get(source, 'No story found.')}")

        print("\nTop World News Stories (One per Source):")
        for source in ACCEPTED_SOURCES:
            print(f"{source}: {world_news.get(source, 'No story found.')}")

    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    main()
