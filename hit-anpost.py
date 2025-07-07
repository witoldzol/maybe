import requests
import pickle
import json
from bs4 import BeautifulSoup

# RESULTS DATA
results_data = []
with open('./results_A92') as f:
    for line in f:
        line = line.strip()
        results_data.append(json.loads(line))
last_key = next(iter(results_data[-1]))

# PERMUTATIONS
with open('./permutations_A92', 'rb') as f:
    permutations_data = pickle.load(f)
index = None
for idx, x in enumerate(permutations_data):
    if x == last_key:
        print('found it ')
        index = idx
if index is None:
    raise 'failed'
print('index of ', last_key, ' ', index)
with open('LAST_PROCESSED_EIRCODE', 'w') as f:
    json.dump({"last_eircode": last_key,"eircode_index":index}, f)
raise 'done'
count = 0
catchup = True
with open('./results_A92', 'a') as fa:
    print('last key', last_key)
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
            new_data = {EIR_CODE: None}
        else:
            html = resp.text
            soup = BeautifulSoup(html, 'lxml')
            all_td_cells = soup.find_all('td')
            # MULTIPLE RESULTS
            if len(all_td_cells) > 1:
                address = []
                for a in all_td_cells:
                    address.append(a.text.strip())
            else:
                address = all_td_cells[-1].text.strip()
            new_data = {EIR_CODE: address}
        json.dump(new_data,fa)
        fa.write('\n')
        count += 1
        if count >= 1000:
            break


print('FINISHED ITERATIOS AFTER 100 records')
