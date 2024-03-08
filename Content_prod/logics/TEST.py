# from modules.nat_tournaments import Nat_Tournaments
# import os
# import json
# with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/associations.json', 'r') as j:
#     associations = json.load(j) # {ass: {rating: , quota: }} 
# Ass_TournRateQuot = {}
# # добавить в Ass_TournRateQuot ассоциации с квотой > 0 в качестве ключей
# # включить в Ass_TournRateQuot турниры нац ассоциаций
# Ass_TournIdType = Nat_Tournaments()
# for ass_n in associations:
#     if ass_n not in Ass_TournRateQuot.keys() and associations[ass_n]['quota'] > 0:
#         for Ass in Ass_TournIdType:
#             if ass_n == Ass:
#                 Ass_TournRateQuot[ass_n] = Ass_TournIdType[Ass]
# for ass_n in Ass_TournRateQuot:
#     Del_tourn = []  # список турниров на удаление
#     for tourn in Ass_TournRateQuot[ass_n]:
#         if tourn[0].find("League") != -1 or tourn[0].find("Cup") != -1: # из нац турниров
#             if tourn[2] == "None" or tourn[0].find("SCup") != -1:   # удалить несуществующие и суперкубки
#                 Del_tourn.append(tourn)
#     for tourn in Del_tourn:
#         Ass_TournRateQuot[ass_n].remove(tourn)    
# print(json.dumps(Ass_TournRateQuot, skipkeys=True, ensure_ascii=False, indent=2))


import datetime
DateNow = datetime.datetime.utcnow()    # текущая дата по UTC
import json
import os
with open((os.path.abspath(__file__))[:-15]+'/cache/answers/fixtures/ESP Cup 22-23 prev.json', 'r') as f:
    file_content = f.read()
answer_dict = json.loads(file_content)
LastInf_date = str([answer_dict['response'][answer_dict['response'].index(elem)]['fixture']['date'] \
    for elem in answer_dict['response'] if 'Final' in elem['league']['round']])[2:-2]
LastInf_date = datetime.datetime(int(LastInf_date[:4]), int(LastInf_date[5:7]), int(LastInf_date[8:10]))
LastInf_date += datetime.timedelta(days=150)
if DateNow >= LastInf_date:
    print(LastInf_date)