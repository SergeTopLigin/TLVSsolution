# определение рейтингов раундов кубка:
# текущего - по текущим standings
# предыдущих - по standings, актуальных на момент окончания последнего матча стадии (/standings_history)


def cup_round_ratings(cup, season, fixtures_dict):
    # cup - в соответствии ass[0] nat_tournaments.py
    # season = YY-YY
    # fixtures_dict - словарь ответа на запрос fixtures кубка
    
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        cup_round_ratings_list = []     # [{round: 'name', type: 'curr'/'prev' last_date: timestamp, rating: float, club_set: [{name: , ID: }, ...]}, ...]
        import os
        import json

# заполнение cup_round_ratings_list раундами
fixtures_rounds = []
for match in fixtures_dict['response']:
    if match['league']['round'].replace(' Replays', '') not in fixtures_rounds:
        played_round = match['league']['round'].replace(' Replays', '')
        fixtures_rounds.append(played_round)
        cup_round_ratings_list.append({'round': played_round, 'type': None, 'last_date': None, 'rating': None, 'club_set': []})

# заполнение cup_round_ratings_list временем окончания последнего матча раунда, определение типа curr/prev раунда
for fixed_round in cup_round_ratings_list:
    last_date = 0
    for match in fixtures_dict['response']:
        if match['league']['round'] == fixed_round['round'] and match['fixture']['timestamp'] + 8000 > last_date:
            last_date = match['fixture']['timestamp'] + 8000
    fixed_round['last_date'] = last_date

# определение type раунда: (возможно, что календарь всех стадий будет опубликован заранее или следующая стадия начнется до конца предыдущей)
# curr: мин last_date при in ['NS', 'TBD', 'PST', 'ABD']
# если curr нет: все раунды - prev
curr_last_date = 3000000000
curr_round = None
for match in fixtures_dict['response']:
    if match['fixture']['status']['short'] in ['NS', 'TBD', 'PST', 'ABD'] and match['fixture']['timestamp'] < curr_last_date:
        curr_last_date = match['fixture']['timestamp']
        curr_round = match['league']['round'].replace(' Replays', '')   # удалить Replays из названия стадии
for fixed_round in cup_round_ratings_list:
    if fixed_round['round'] == curr_round:
        fixed_round['type'] = 'curr'
        curr_last_date = fixed_round['last_date']
# prev: last_date до curr
for fixed_round in cup_round_ratings_list:
    if fixed_round['last_date'] < curr_last_date:
        fixed_round['type'] = 'prev'
# null: last_date после curr - значение из прошлого раздела

# заполнение списка club_set[{name: , ID: }, ...] раунда
for fixed_round in cup_round_ratings_list:
    for match in fixtures_dict['response']:
        if match['league']['round'] == fixed_round['round']:
            if {'name': match['teams']['home']['name'], 'id': match['teams']['home']['id']} not in fixed_round['club_set']:
                fixed_round['club_set'].append({'name': match['teams']['home']['name'], 'id': match['teams']['home']['id']})
            if {'name': match['teams']['away']['name'], 'id': match['teams']['away']['id']} not in fixed_round['club_set']:
                fixed_round['club_set'].append({'name': match['teams']['away']['name'], 'id': match['teams']['away']['id']})

# определение рейтинга стадии: total Cup stage clubs SUM(pts+1.2) in TL standigs / Number of clubs in the Cup stage
# для curr: по текущим standings
# для prev: по standings, актуальным на момент окончания последнего матча стадии
for fixed_round in cup_round_ratings_list:
    if fixed_round['type'] == 'curr':
        with open('final_standings.json', 'r', encoding='utf-8') as j:
            standings = json.load(j)
    if fixed_round['type'] == 'prev':
        round_last_date = str(datetime.datetime.utcfromtimestamp(fixed_round['last_date']))[:10]
        use_standings_date = '2100-01-01'    # установить дату первого standings в /standings_history
        for standings_file in os.listdir((os.path.abspath(__file__))[:-13]+'/TL_VS_solution/Content_prod/cache/sub_results/standings_history'):
            standings_date = standings_file[10:20]
            if 'standings' in standings_file and standings_date < use_standings_date:
                use_standings_date = standings_date
        for standings_file in os.listdir((os.path.abspath(__file__))[:-13]+'/TL_VS_solution/Content_prod/cache/sub_results/standings_history'):
            standings_date = standings_file[10:20]
            if 'standings' in standings_file and standings_date < round_last_date and standings_date > use_standings_date:
                use_standings_date = standings_date
        with open((os.path.abspath(__file__))[:-13]+'/TL_VS_solution/Content_prod/cache/sub_results/standings_history/standings '\
            +str(use_standings_date)+'.json', 'r', encoding='utf-8') as j:
            standings = json.load(j)
        

# print(json.dumps(cup_round_ratings_list, skipkeys=True, ensure_ascii=False, indent=2))
# возможно не следует пользоваться данными и файла, проще пересчитывать весь кубок по текущему fixturess        
#         # формирование cup_round_ratings_list из файла /cup_round_ratings 
#         for cup_round_file in os.listdir((os.path.abspath(__file__))[:-36]+'/cache/sub_results/cup_round_ratings'):
#             if cup_round_file.find(cup) != -1 and cup_round_file.find(season) != -1:
#                 with open((os.path.abspath(__file__))[:-36]+'/cache/sub_results/cup_round_ratings/'+cup_round_file, 'r', encoding='utf-8') as j:
#                     cup_round_ratings_list = json.load(j)

        # # фиксирование раундов из fixtures_dict в cup_round_ratings_list
        # # работает как для списка из cup_round_file, так и для пустого списка
        # fixtures_rounds = []
        # for match in fixtures_dict['response']:
        #     if match['league']['round'].replace(' Replays', '') not in fixtures_rounds:
        #         fixtures_rounds.append(match['league']['round'].replace(' Replays', ''))
        # for played_round in fixtures_rounds:
        #     add_round = 1
        #     for fixed_round in cup_round_ratings_list:
        #         if played_round == fixed_round['round']:
        #             add_round = 0
        #     if add_round == 1:
        #         cup_round_ratings_list.append({'round': played_round, 'type': None, 'last_date': None, 'rating': None, 'clubID_set': []})

        # # проверка наличия рейтингов предыдущих раундов в cup_round_ratings_list
        # # если раундов в cup_round_file не было - рейтингов этих райндов тоже нет
        # # при изменении типа раунда с prev на curr - рейтинг надо пересчитать
        # for fixed_round in cup_round_ratings_list:
        #     if fixed_round['type'] != 'prev'

        # формирование cup_round_ratings_list из fixtures_dict


        # расчет рейтингов отсутствующих предыдущих раундов

        # расчет рейтинга текущего раунда (TL_standings каждый день изменяется)

        # запись данных в файл /cup_round_ratings


    except:

        # запись ошибки/исключения в переменную через временный файл
        import traceback
        with open("bug_file.txt", 'w+') as f:
            traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
            f.seek(0)                       # установка курсора в начало временного файла
            bug_info = f.read()

        # отправка bug_file в репозиторий GitHub и на почту
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'bug_files', 'bug_file', bug_info)
        from modules.bug_mail import bug_mail
        bug_mail(str(mod_name), bug_info)