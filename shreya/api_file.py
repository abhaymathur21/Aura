# api_key = "d098d69582614ec2a040d16f2653a97f"
import requests

url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "in",
    "apiKey": "d098d69582614ec2a040d16f2653a97f"
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
