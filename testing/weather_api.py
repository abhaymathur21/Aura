import requests
api_key = "b5f1f8b3ce854380f043e7dd3aac0962"
location=input("Enter Location: ")
url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    temp = data["main"]
    print("Temperature: ",temp)
    temp = data["weather"]
    print("Weather: ",temp)
else:
    raise Exception(f"Failed to fetch temperature data: {response.text}")