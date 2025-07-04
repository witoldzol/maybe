import csv
import json
with open('./routing-keys.csv') as f:
    data = csv.DictReader(f, delimiter='\t')
    with open('./routing-keys.json', 'w') as fb:
        json.dump(list(data), fb)
