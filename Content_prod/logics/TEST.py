import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/AUT League 2023.json', 'r') as f:
    prev_file = f.read()
answer_dict = json.loads(prev_file)

print(prev_file)