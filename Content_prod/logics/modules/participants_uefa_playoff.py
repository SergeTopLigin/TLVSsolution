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
        # 1,2: для сезона 23/24 и раньше при переходе клуба в турнир рангом ниже после групповой стадии: оба критерия для групповых матчей 
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
        import os
        import json
        import random
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        from modules.runner_push import runner_push
        from modules.apisports_key import api_key    # модуль с ключом аккаунта api
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
            
            # формирование standings турниров из которых возможны переходы клубов с 3-х мест групп
            if int(season[:2]) < 24:
                if 'UEL' in tourn:
                    if 'UCL '+season+' stan.json' not in os.listdir((os.path.abspath(__file__))[:-44]+'/cache/answers/standings'):
                        UCLstan = api_key("/standings?league=2&season=20"+season[:2])
                        gh_push(str(mod_name), 'standings', 'UCL '+season+' stan.json', UCLstan)
                        runner_push(str(mod_name), 'standings', 'UCL '+season+' stan.json', UCLstan)
                    with open((os.path.abspath(__file__))[:-44]+'/cache/answers/standings/UCL '+season+' stan.json', 'r') as j:
                        drop_tourn_standings = json.load(j)
                if 'UECL' in tourn:
                    if 'UEL '+season+' stan.json' not in os.listdir((os.path.abspath(__file__))[:-44]+'/cache/answers/standings'):
                        UELstan = api_key("/standings?league=3&season=20"+season[:2])
                        gh_push(str(mod_name), 'standings', 'UEL '+season+' stan.json', UELstan)
                        runner_push(str(mod_name), 'standings', 'UEL '+season+' stan.json', UELstan)
                    with open((os.path.abspath(__file__))[:-44]+'/cache/answers/standings/UEL '+season+' stan.json', 'r') as j:
                        drop_tourn_standings = json.load(j)
            
            # набор и сортировка клубов стадий для заполнения квоты турнира
            reg_time = ['ET', 'BT', 'P', 'FT', 'AET', 'PEN']  # список статусов окончания основного времени
            for stage in playoff_rounds:
                # набор stage_set [{'club': , 'id': ,'pts': , 'dif': , 'pl': , 'pts/pl': , 'dif/pl': , 'TL_rank': , 'random_rank': }]
                stage_set = []
                for fixture in tourn_fixtures['response']:
                    if fixture['league']['round'] == stage and fixture['teams']['home']['id'] not in [club['id'] for club in stage_set]\
                    and fixture['teams']['home']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['home']['name'], 'id': fixture['teams']['home']['id'],\
                         'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
                    if fixture['league']['round'] == stage and fixture['teams']['away']['id'] not in [club['id'] for club in stage_set]\
                    and fixture['teams']['away']['id'] not in [club['id'] for club in participants]:
                        stage_set.append({'club': fixture['teams']['away']['name'], 'id': fixture['teams']['away']['id'],\
                         'pts': 0, 'dif': 0, 'pl': 0, 'pts/pl': None, 'dif/pl': None, 'TL_rank': None, 'random_rank': None})
                # набор критериев и сортировка stage_set
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
                    # для сезона 23/24 и ранее: набор очков и разниц из групп других турниров УЕФА (для перешедших с 3-х мест) с кор коэффициентами 
                    if int(season[:2]) < 24:
                        for group in drop_tourn_standings['response'][0]['league']['standings']:
                            for rank in group:
                                if rank['team']['id'] == club['id']:
                                    club['pl'] += rank['all']['played']
                                    club['pts'] += rank['points'] *2
                                    if rank['goalsDiff'] > 0:   club['dif'] += rank['goalsDiff'] *2
                                    else:                       club['dif'] += rank['goalsDiff'] /2
                    club['pts/pl'] = club['pts'] / club['pl']
                    club['dif/pl'] = club['dif'] / club['pl']
                    if club['club'] in TL_standings:
                        club['TL_rank'] = [TL_standings[TL_club]['TL_rank'] for TL_club in TL_standings if TL_club == club['club']][0]
                    else:
                        club['TL_rank'] = -5
                    club['random_rank'] = random.random()
                stage_set.sort(key=lambda crit: (crit['pts/pl'], crit['dif/pl'], crit['TL_rank'], crit['random_rank']), reverse=True)

                if len(stage_set) == quota:
                    participants = [{'club': club['club'], 'id': club['id']} for club in stage_set]
                    break

        

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
