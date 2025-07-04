import requests

EIR_CODE = "D15X653"

# get KEY
with open('EIRCODE_KEY') as f:
    API_KEY = f.read()
    print('read eircode key: ', API_KEY)

# validate url
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }
url = f"https://api-finder.eircode.ie/Latest/finderfindaddress?key={API_KEY}&address={EIR_CODE}&language=en&geographicAddress=true&clientVersion=e98fe302"
resp = requests.get(url, headers=headers)
resp.raise_for_status()
print(resp.json())
