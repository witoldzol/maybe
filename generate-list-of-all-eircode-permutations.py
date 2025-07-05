from contants import ROUTING_KEYS
import string
import json
first_key = list(ROUTING_KEYS)[0]

def is_dublin(key: str) -> bool:
    return key[0].upper() == 'D'

permutations = []
if not is_dublin(first_key):
    ALL = string.ascii_uppercase + string.digits
    DIGITS = string.digits
    for first in ALL:
        for second in ALL:
            for third in DIGITS:
                for fourth in DIGITS:
                    permutations.append(first+second+third+fourth)
final = {}
for unique_key in permutations:
    final[f"{first_key}{unique_key}"] = {}
with open(f'permutations_{first_key}', 'w') as f:
    json.dump(final, f)
print('number of combinations :')
print(len(final))
