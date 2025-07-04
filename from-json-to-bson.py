import bson
import json
with open('./out') as f:
    data = json.load(f)
b_data = bson.dumps(data)
with open('./out_b', 'wb') as fb:
    fb.write(b_data)
