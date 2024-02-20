import os
import json
with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/AUT League 2023.json', 'r', encoding='utf-8') as j:
    # print(json.dumps(eval(f.read()), skipkeys=True, ensure_ascii=False, indent=2))
    standings_dict = json.load(j)
# print(standings_dict["response"][0]["league"]["standings"][0][0]["team"]["name"])
for club in standings_dict["response"][0]["league"]["standings"][0]:
    print(club["team"]["name"])


# # удаление файлов json из каталога
# dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
# for file in dir_standings:
#     if 'json' in file:
#         os.remove((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file)

# # кодирование .txt в .json
# dir_standings = os.listdir((os.path.abspath(__file__))[:-15]+'/cache/answers/standings')
# for file in dir_standings:
#     if 'txt' in file:
#         with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file, 'r', encoding='utf-8') as f:
#             with open((os.path.abspath(__file__))[:-15]+'/cache/answers/standings/'+file[:-4]+'.json', 'w', encoding='utf-8') as j:
#                 json.dump(json.loads(f.read()), j, skipkeys=True, ensure_ascii=False, indent=2)
