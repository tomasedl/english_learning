import json
import random

file = open("words.json")

data = json.load(file)

print(data)

for item in data:
    print(item, ":", data[item])
    print("".join(random.sample(item, len(item))))





