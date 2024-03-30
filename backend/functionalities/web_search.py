import requests
from bs4 import BeautifulSoup

def scrape_google_search(query, num_results):
    """
    Scrapes Google search results using BeautifulSoup.

    Args:
        query (str): The search query to use.
        num_results (int, optional): The number of results to scrape. Defaults to 5.

    Returns:
        list: A list of URLs for the top results.

    Raises:
        Exception: If there is an issue with the request or parsing.
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"  # Mimic a browser
    headers = {"User-Agent": user_agent}

    try:
        google_url = f"https://www.google.com/search?q={query}"
        response = requests.get(google_url, headers=headers)
        response.raise_for_status()  # Raise exception for non-200 status codes

        soup = BeautifulSoup(response.content, "lxml")

        # Extract links within result divs (might change based on Google's structure)
        results = soup.find_all("div", class_="g")[:num_results]
        links = [result.find("a", href=True)["href"] for result in results if result.find("a", href=True)]

        return links

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


# user_query = input("Enter your search query: ")
# scraped_links = scrape_google_search(user_query)

# if scraped_links:
#     print(f"\nTop {len(scraped_links)} results for '{user_query}':")
#     for link in scraped_links:
#         print(link)
# else:
#     print("No results found for your query.")

