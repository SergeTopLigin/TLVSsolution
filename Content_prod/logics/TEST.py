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

# uefa_standings.py: если в словаре есть клуб несоответсвующий ни одному из имен в каталоге /standings - создать bug_file
                    # for line in f:  # цикл по строкам
                    #     end_substr = 0
                    #     while True:     # бесконечный цикл
                    #         if line.find('name":"',end_substr) ==-1:
                    #             break
                    #         kursor = line.find('name":"',end_substr) +7    # переместить курсор перед искомой подстрокой
                    #         end_substr = line.find('","',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                    #         if club == line[kursor:end_substr]:
                    #             find_club = 1
                    #             break

# # сортировка вложенного словаря по значению
# TL_standings = {
#     "ManCity":{
#         "IDapi": 1,
#         "nat": "ENG"
#     },
#     "Bayern":{
#         "IDapi": 2,
#         "nat": "GER"
#     },
#     "Real":{
#         "IDapi": 3,
#         "nat": "ESP"
#     }
# }
# TL_standings = dict(sorted(TL_standings.items(), key=lambda x: x[1].get("IDapi"), reverse=True))
