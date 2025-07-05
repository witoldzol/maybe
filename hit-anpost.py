import requests
import json
from bs4 import BeautifulSoup

with open('./results_A92') as f:
    results_data = json.load(f)
    last_key = list(results_data)[-1]
with open('./permutations_A92') as f:
    permutations_data = json.load(f)

catchup = True
for EIR_CODE in permutations_data:
    if catchup:
        if EIR_CODE == last_key:
            print(f"found last key = {last_key}, continuing processing keys")
            catchup = False
            continue
        else:
            continue
    print(f'processing key {EIR_CODE}')
    url = f'https://forms.anpost.ie/enquiry/SenderDetails/SearchForAddress/?findPostalAddress={EIR_CODE}'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Content-Type': 'application/json' }
    resp = requests.get(url, headers=headers)
    if "No matching" in resp.text:
        print(f"no match for {EIR_CODE}")
        results_data[EIR_CODE] = None
    else:
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        all_td_cells = soup.find_all('td')
        # handle issue
        if len(all_td_cells) != 1:
            print(html)
            with open('results_A92', 'w') as f:
                json.dump(results_data, f)
            raise Exception('Hey, I found more/less than one table cell with address')
        address = all_td_cells[0].text.strip()
        routing_key = EIR_CODE[:3]
        # check address contains expected eirccode
        if routing_key not in address:
            with open('results_A92', 'w') as f:
                json.dump(results_data, f)
            raise Exception(f'Hey, ROUTING KEY {routing_key} was not found in the address = {address}')
        results_data[EIR_CODE] = address
        break
with open('results_A92', 'w') as f:
    json.dump(results_data, f)

print('FINISHED ITERATIOS')
