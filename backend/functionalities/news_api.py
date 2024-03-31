import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "in",
    "apiKey": os.environ["NEWS_API_KEY"],
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    articles = data['articles']
    for article in articles:
        try:
            print(article['url'])
        except:
            print("")
else:
    print("Failed to retrieve headlines:", response.status_code)
