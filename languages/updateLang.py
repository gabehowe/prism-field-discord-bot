import json
import os

jsonArray = {}

for filename in os.listdir("../languages"):
    if not filename.endswith("json"):
        continue
    if filename.startswith("lang"):
        continue

    with open("../languages/" + filename) as file:
        jsonArray[filename[:-5]] = (json.load(file))

with open("lang.json", "w+", encoding="utf-8") as lang:
    lang.write(json.dumps(jsonArray))
