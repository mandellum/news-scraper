import requests

# Define accepted sources
ACCEPTED_SOURCES = {"Associated Press", "Reuters", "BBC"}

def get_filtered_news(api_key, query, date):
    """Fetch and filter top news from AP, Reuters, and BBC."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "tbs": f"cdr:1,cd_min:{date},cd_max:{date}",
        "hl": "en",
        "gl": "us",
        "num": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    return [
        f"{article['title']} - {article['source']} ({article['link']})"
        for article in data.get("news_results", [])
        if article.get("source") in ACCEPTED_SOURCES
    ][:2]

def main():
    # Ask for user input
    api_key = input("Enter your SerpAPI Key: ").strip()
    date = input("Enter the date (YYYY-MM-DD) for the news: ").strip()

    if not api_key:
        print("API Key is required. Exiting...")
        return

    try:
        # Fetch and filter news
        us_news = get_filtered_news(api_key, "top news in the US", date)
        world_news = get_filtered_news(api_key, "world news", date)

        # Output results
        print("\nTop US News Stories (From AP, Reuters, BBC):")
        for i, story in enumerate(us_news, 1):
            print(f"{i}. {story}")

        print("\nTop World News Stories (From AP, Reuters, BBC):")
        for i, story in enumerate(world_news, 1):
            print(f"{i}. {story}")

    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    main()
