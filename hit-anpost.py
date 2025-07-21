import requests
import queue
import pickle
import json
from bs4 import BeautifulSoup


def file_writer_worker(q, filename):
    with open(filename, "a") as f:
        while True:
            try:
                result = q.get(timeout=1)
                if result is None:
                    print("File writer received None, stopping work")
                    break
                json.dump(result, f)
                f.write("\n")
                q.task_done()
            except queue.Empty:
                pass  # empty, try again


def update_last_processed_item(last_key: str = None, index: int = None):
    if last_key is None:
        raise Exception("last_key is None")
    if last_key_index is None:
        raise Exception("last_key_index is None")
    with open("LAST_PROCESSED_EIRCODE", "w") as f:
        offset = {"last_eircode": last_key, "eircode_index": index}
        json.dump(offset, f)


# PERMUTATIONS
with open("./permutations_A92", "rb") as f:
    permutations_data: list[str] = pickle.load(f)

# LOAD LAST PROCESSED EIRCODE
with open("LAST_PROCESSED_EIRCODE", "r") as f:
    offset_info = json.load(f)
    last_key = offset_info["last_eircode"]
    index = offset_info["eircode_index"]
    # move by one to avoid duplication
    index += 1
# if permutations_data[index] != last_key:
#     raise Exception(f"Last processed index = {index} doesnt match the last processed EIRCODE = {last_key}")

MAX_ITEMS_TO_PROCESS = 10
count = 0
try:
    with open("./results_A92", "a") as fa:
        for idx, EIR_CODE in enumerate(permutations_data[index:]):
            last_key_processed = EIR_CODE
            last_key_index = idx
            print(f"processing key {EIR_CODE}")
            url = f"https://forms.anpost.ie/enquiry/SenderDetails/SearchForAddress/?findPostalAddress={EIR_CODE}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Content-Type": "application/json",
            }
            resp = requests.get(url, headers=headers)
            if "No matching" in resp.text:
                print(f"no match for {EIR_CODE}")
                new_data = {EIR_CODE: None}
            else:
                html = resp.text
                soup = BeautifulSoup(html, "lxml")
                all_td_cells = soup.find_all("td")
                # MULTIPLE RESULTS
                if len(all_td_cells) > 1:
                    address = []
                    for a in all_td_cells:
                        address.append(a.text.strip())
                else:
                    address = all_td_cells[-1].text.strip()
                new_data = {EIR_CODE: address}
            json.dump(new_data, fa)
            fa.write("\n")
            count += 1
            if count >= MAX_ITEMS_TO_PROCESS:
                break
finally:
    update_last_processed_item(last_key_processed, last_key_index + index)

print("FINISHED ITERATIOS AFTER 100 records")
