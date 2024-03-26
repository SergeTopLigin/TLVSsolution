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
        
        # словарь стадий
        rounds = {}    # {round: {'last_date': , 'status': }}
        for fixture in tourn_fixtures['response']:
            if fixture['league']['round'] not in rounds or\
            fixture['fixture']['timestamp'] > [rounds[stage]['last_date'] for stage in rounds if fixture['league']['round'] == stage][0]:
                rounds[fixture['league']['round']] = {'last_date': fixture['fixture']['timestamp'], 'status': fixture['fixture']['status']['short']}
        # определение текущей стадии
        cancelled = ['FT', 'AET', 'PEN', 'CANC', 'AWD', 'WO']   # список статусов завершения
        rounds_cont = [{stage: rounds[stage]['last_date']} for stage in rounds if rounds[stage]['status'] not in cancelled]   # незавершенные стадии [{round: last_date}, ]
        curr_round = min(rounds_cont, key = rounds_cont.get)    # текущая стадия - ранняя из незавершенных
        # выборка стадий только playoff и не позднее текущей
        group_rounds = [{stage: rounds[stage]['last_date']} for stage in rounds if 'Group' in stage]   # все групповые rounds
        last_group_round_time = max(group_rounds.values())    # время последнего группового round

        

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
