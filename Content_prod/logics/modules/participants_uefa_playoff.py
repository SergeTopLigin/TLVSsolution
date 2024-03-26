# определение участников из playoff set турнира UEFA
# возвращает список участников = [{club: , id: }, ...]

# текущая стадия (1/8, 1/4 итд): последняя несыгранная, если известны все ее участники, или финал
# если количество участников текущей стадии равно квоте: все участники текущей стадии
# если количество участников текущей стадии больше квоты: победитель турнира или лучшие среди участников текущей стадии
# если количество участников текущей стадии меньше квоты: все участники текущей стадии + лучшие среди участников предыдущей стадии
# критерии определения лучших участников стадии:
    # 1. PTS/PL
    # 2. DIF/PL
        # 1,2: от групповых матчей до текущей стадии
        # 1,2: для сезона 23/24 при переходе клуба в турнир рангом ниже после групповой стадии: оба критерия для групповых матчей 
            # увеличиваются х2 (или уменьшаются /2 для отрицательных значений)
    # 3. TL standings
    # 4. random

# определение участников происходит по fixtures и standings 

def participants_uefa_playoff(tourn, tourn_id, season, quota):
    # tourn = tournaments.json['UEFA']['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json['UEFA']['tournaments'][tourn]['id']
    # season = tournaments.json['UEFA']['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json['UEFA']['tournaments'][tourn]['quota']

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        best_define = []    # список с критериями определения лучших best_define = [{'club': , 'id': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
        import os
        import json
        import random
        with open((os.path.abspath(__file__))[:-44]+'/cache/sub_results/final_standings.json', 'r') as j:
            TL_standings = json.load(j)

        # актуализация fixtures и standings турнира
        from modules.uefa_tourn_files import uefa_tourn_files
        uefa_tourn_files(tourn, season, tourn_id, 'playoff')
        
        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-44]+'/cache/answers/fixtures'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1
                with open((os.path.abspath(__file__))[:-44]+'/cache/answers/fixtures/'+tourn_file, 'r') as j:
                    tourn_fixtures = json.load(j)
                break
        
        if file_find == 1:
            # словарь стадий
            rounds = {}    # {round: {'last_date': , 'status': }}
            for fixture in tourn_fixtures['response']:
                if fixture['league']['round'] not in rounds or\
                fixture['fixture']['timestamp'] > [rounds[stage]['last_date'] for stage in rounds if fixture['league']['round'] == stage][0]:
                    rounds[fixture['league']['round']] = {'last_date': fixture['fixture']['timestamp'], 'status': fixture['fixture']['status']['short']}
            # определение времени текущей стадии
            cancelled = ['FT', 'AET', 'PEN', 'CANC', 'AWD', 'WO']   # список статусов завершения
            rounds_cont_time = {stage: rounds[stage]['last_date'] for stage in rounds if rounds[stage]['status'] not in cancelled}   # время незавершенных стадий
            curr_round_time = min(rounds_cont_time.values())    # время текущей стадии - ранней из незавершенных
            # определение времени последнего группового round
            group_rounds = {stage: rounds[stage]['last_date'] for stage in rounds if 'Group' in stage}   # все групповые rounds
            last_group_round_time = max(group_rounds.values())    # время последнего группового round
            # выборка стадий только playoff и не позднее текущей
            playoff_rounds = {stage: rounds[stage]['last_date'] for stage in rounds if rounds[stage]['last_date'] > last_group_round_time and\
             rounds[stage]['last_date'] <= curr_round_time}
            # выборка стадий от групповых матчей до текущей стадии
            main_rounds = list(group_rounds.keys()) + list(playoff_rounds.keys())
            # сортировка стадий плейофф от текущей в прошлое
            playoff_rounds = sorted(playoff_rounds, key=lambda stage: playoff_rounds[stage], reverse=True)
            
            reg_time = ['ET', 'BT', 'P', 'FT', 'AET', 'PEN']  # список статусов окончания основного времени
            for stage in playoff_rounds:
                # набор stage_set [{'club': , 'id': ,'pts': , 'dif': , 'pl': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
                stage_set = []
                for fixture in tourn_fixtures['response']:
                    if fixture['league']['round'] == stage and fixture['teams']['home']['id'] not in [stage['id'] for stage in stage_set]\
                    and fixture['teams']['home']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['home']['name'], 'id': fixture['teams']['home']['id'],\
                         'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
                    if fixture['league']['round'] == stage and fixture['teams']['away']['id'] not in [stage['id'] for stage in stage_set]\
                    and fixture['teams']['away']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['away']['name'], 'id': fixture['teams']['away']['id'],\
                         'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
                # сортировка stage_set
                for club in stage_set:
                    for fixture in tourn_fixtures['response']:
                        if fixture['league']['round'] in main_rounds and club['id'] == fixture['teams']['home']['id']\
                         and fixture['fixture']['status']['short'] in reg_time:
                            club['pl'] += 1
                            if fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away']:     club['pts'] += 3
                            elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:  club['pts'] += 1
                            club['dif'] += fixture['score']['fulltime']['home'] - fixture['score']['fulltime']['away']
                        if fixture['league']['round'] in main_rounds and club['id'] == fixture['teams']['away']['id']\
                         and fixture['fixture']['status']['short'] in reg_time:
                            club['pl'] += 1
                            if fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away']:     club['pts'] += 3
                            elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:  club['pts'] += 1
                            club['dif'] += fixture['score']['fulltime']['away'] - fixture['score']['fulltime']['home']


                if len(stage_set) == quota:

        

        return(participants)

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
        
        return([])
