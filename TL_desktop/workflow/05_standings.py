# формирование standings
# uefa_standings.py > sub_result/uefa_standings.json
# TL_standings.py > sub_result/TL_standings.json
# standings.py > sub_result/final_standings.json, sub_result/standings_history/standings YYYY-MM-DD.json
# для объединения uefa_standings и TL_standings в final_standings временно прибавить к рейтингам клубов в обоих standings по +5
# это выведет в + даже самое крупное недавнее поражение в TL

# определение влияния UEFA club rankings на текущий TL standings
import datetime
# TL_start_date: 100% UEFA club rankings + 0% TL standings
TL_start_date = datetime.datetime(2024, 8, 1)   # дата начала обработки игр TL
curr_time = datetime.datetime.utcnow()          # текущее время
# каждый следующий день в 0:00 1/365 переходит в standings
# определение количества полных дней после TL_start_date по UTC
if curr_time <= TL_start_date:
    Days_after_start = 0
elif curr_time > TL_start_date + datetime.timedelta(days=365):
    Days_after_start = 365
else: 
    Days_after_start = int((curr_time-TL_start_date)//datetime.timedelta(days=1))
# коэффициент влияния rate TL standings на итоговый rate клубов
TL_Influence = (1/365)*Days_after_start
# коэффициент влияния UEFA club rankings на итоговый rate клубов
UEFA_Influence = 1-TL_Influence

# формирование исходных uefa_standings и TL_standings при необходимости
import json
import os
if TL_Influence > 0:
    # декодирование из файла TL_standings
    with open((os.path.abspath(__file__))[:-25]+'/cache/TL_standings.json', 'r', encoding='utf-8') as j:
        TL_standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
if UEFA_Influence > 0:
    # декодирование из файла uefa_standings
    with open((os.path.abspath(__file__))[:-25]+'/cache/uefa_standings.json', 'r', encoding='utf-8') as j:
        uefa_standings = json.load(j)   # {club: {IDapi: , nat: , TL_rank: , visual_rank: }}
    
# формирование словаря final_standings
if UEFA_Influence == 1:
    final_standings = uefa_standings
elif TL_Influence == 1:
    final_standings = TL_standings
else:   # объединение uefa_standings и TL_standings
    final_standings = {}
    # объединить клубы из обоих словарей
    final_standings_list = list(uefa_standings.keys()) + list(TL_standings.keys())  # список клубов обоих standings
    final_standings_list = list(set(final_standings_list))  # убрать повторы через множество
    for club in final_standings_list:
        if club in TL_standings and club in uefa_standings:
            final_standings[club] = TL_standings[club]
            final_standings[club]['TL_rank'] = \
            round((TL_standings[club]['TL_rank']+5)*TL_Influence + (uefa_standings[club]['TL_rank']+5)*UEFA_Influence - 5, 2)
        elif club in TL_standings:
            final_standings[club] = TL_standings[club]
            final_standings[club]['TL_rank'] = round((TL_standings[club]['TL_rank']+5)*TL_Influence - 5, 2)
        elif club in uefa_standings:
            final_standings[club] = uefa_standings[club]
            final_standings[club]['TL_rank'] = round((uefa_standings[club]['TL_rank']+5)*UEFA_Influence - 5, 2)
            final_standings[club]['played'] = 0
    # visual_rank
    TL_rank_max = max([final_standings[club]['TL_rank'] for club in final_standings])
    TL_rank_min = min([final_standings[club]['TL_rank'] for club in final_standings])
    for club in final_standings:
        final_standings[club]['visual_rank'] = int(round(100 * (final_standings[club]['TL_rank'] - TL_rank_min) / (TL_rank_max - TL_rank_min), 0))
    # сортировка final_standings с учетом buffer: 
    # в main_stands попадают:
    # в первые 122 дня после TL_start_date - все клубы
    if curr_time < TL_start_date + datetime.timedelta(days=123):
        main_stands = {club:final_standings[club] for club in final_standings}
        main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        buffer_1pl = {}
        buffer_0pl = {}
    # с 123 по 244 день после TL_start_date - клубы, сыгравшие 1 игру
    elif TL_start_date + datetime.timedelta(days=122) < curr_time < TL_start_date + datetime.timedelta(days=245):
        main_stands = {club:final_standings[club] for club in final_standings if final_standings[club]['played'] > 0}
        main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        buffer_1pl = {}
        buffer_0pl = {club:final_standings[club] for club in final_standings if final_standings[club]['played'] == 0}
        buffer_0pl = dict(sorted(buffer_0pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
    # с 245 по 365 день после TL_start_date - клубы, сыгравшие 2 игры
    elif TL_start_date + datetime.timedelta(days=244) < curr_time < TL_start_date + datetime.timedelta(days=366):
        main_stands = {club:final_standings[club] for club in final_standings if final_standings[club]['played'] > 1}
        main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        buffer_1pl = {club:final_standings[club] for club in final_standings if final_standings[club]['played'] == 1}
        buffer_1pl = dict(sorted(buffer_1pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        buffer_0pl = {club:final_standings[club] for club in final_standings if final_standings[club]['played'] == 0}
        buffer_0pl = dict(sorted(buffer_0pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
    # переинициализация TL-standings
    final_standings = {}
    for club in main_stands:
        final_standings[club] = main_stands[club]
        final_standings[club]['buffer'] = False
    for club in buffer_1pl:
        final_standings[club] = buffer_1pl[club]
        final_standings[club]['buffer'] = True
    for club in buffer_0pl:
        final_standings[club] = buffer_0pl[club]
        final_standings[club]['buffer'] = True

with open((os.path.abspath(__file__))[:-25]+'/cache/final_standings.json', 'w', encoding='utf-8') as j:
    json.dump(final_standings, j, skipkeys=True, ensure_ascii=False, indent=2)

CreateDate = str(datetime.datetime.utcnow())[:19].replace(":", "-").replace(' ','_')
with open((os.path.abspath(__file__))[:-25]+'/cache/standings_history/standings '+CreateDate[:-9]+'.json', 'w', encoding='utf-8') as j:
    json.dump(final_standings, j, skipkeys=True, ensure_ascii=False, indent=2)


# # формирование строки из словаря в читабельном виде
# final_standings_str = ''   # github принимает только str для записи в файл
# rank = 1
# for club in final_standings:
#     final_standings_str += "{0:>2}  {1:25}{2:3.0f}   {3:5.2f}    {4}".\
#     format(str(rank), club, final_standings[club]['visual_rank'], final_standings[club]['TL_rank'], \
#         final_standings[club]['nat']) + '\n'
#     rank += 1

# # выгрузка standings.txt в репо: /content и /content_commits  и на runner: /content
# gh_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
# runner_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
# gh_push(str(mod_name), 'content_commits', 'standings.txt', final_standings_str)