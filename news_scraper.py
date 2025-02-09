import requests

# Define accepted sources (adjusted for exact names in the API response)
ACCEPTED_SOURCES = {"The Associated Press", "Reuters", "BBC.com"}

def get_filtered_news(api_key, query, date):
    """Fetch and filter top news from AP, Reuters, and BBC."""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "tbs": f"cdr:1,cd_min:{date},cd_max:{date}",  # Filter by date
        "hl": "en",
        "gl": "us",
        "num": 10  # Get more stories to ensure we get results
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Print the raw response data for debugging (you can remove this line later)
    # print("Raw API Response:", data)

    # Ensure the 'news_results' key exists and is properly formatted
    if 'news_results' not in data:
        print("Error: 'news_results' key not found in the response.")
        return []

    # Ensure filtering works on the source name
    filtered_news = []
    for article in data.get("news_results", []):
        source_name = article.get("source", {}).get("name", "")
        # Check if the source name is in the accepted sources
        if source_name in ACCEPTED_SOURCES:
            filtered_news.append(f"{article['title']} - {source_name} ({article['link']})")

    return filtered_news[:2]  # Return top 2 stories

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
        if us_news:
            print("\nTop US News Stories (From AP, Reuters, BBC):")
            for i, story in enumerate(us_news, 1):
                print(f"{i}. {story}")
        else:
            print("\nNo US news found from AP, Reuters, or BBC.")

        if world_news:
            print("\nTop World News Stories (From AP, Reuters, BBC):")
            for i, story in enumerate(world_news, 1):
                print(f"{i}. {story}")
        else:
            print("\nNo world news found from AP, Reuters, or BBC.")

    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    main()
