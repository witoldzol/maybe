import requests
EIR_CODE = "D15X653"
url = f'https://forms.anpost.ie/enquiry/SenderDetails/SearchForAddress/?findPostalAddress={EIR_CODE}'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Content-Type': 'application/json' }
resp = requests.get(url, headers=headers)
print(resp.text)
