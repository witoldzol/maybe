import requests
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
url = "https://api-finder.eircode.ie/Latest/findergetidentity"
resp = requests.get(url, headers=headers)
resp.raise_for_status()
KEY = resp.json()["key"]
print("setting api key: ", KEY)
with open('EIRCODE_KEY', 'w') as f:
    f.write(KEY)
