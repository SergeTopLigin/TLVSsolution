import os
import json
# dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
# for file in dir_standings:
#     print(file)
with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/AUT League 2023.txt', 'r') as f:
    # dict_standings = dict(f.read())
    print(json.dumps(f.read(), skipkeys=True, ensure_ascii=False, indent=2))
