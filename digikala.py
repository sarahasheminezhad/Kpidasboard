import requests
import json

url = "https://api.digikala.com/v1/search/"
params = {"q": "", "page": 1}
headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

response = requests.get(url, params=params, headers=headers)

data = response.json()

# چاپ زیبا و قابل خواندن
print(json.dumps(data, indent=4, ensure_ascii=False))
