'''
функция games_main_finish.py:
определение игр expected, начинающихся после момента расчета (worktimes.json), с только что определенными participants на месяц вперед

формирование и хранение результатов игр:
игры хранятся в словаре {club: [games{}]}
в список по ключу клуба попадает каждая игра этого клуба в рамках TL
каждая игра это словарь, включающий ключи: соперник, дата, счет, рейтинг соперника на момент игры и др характеристики для расчета standings клуба

games = {club_id: 
    [
        {
        'club_name':
        'date': 'date'              begining date and time
        'match': 'home - away G:G'              90' result
        'game_status': 'fixed/unfinished/expected'   
            'fixed' - фиксируемая, с завершенным основным временем
            'unfinished' - фиксируемая, начавшаяся, с незавершенным основным временем
            'expected' - ожидаемая по текущему списку участников                

        'opponent': 'opponent'
        'opp_id':
        'result': 'win/draw/lose'   90'
        'opp_TLrate': float         on matchday
        'goalDiff': int             90'
        'timestamp': float          datetime in sec
        
        'fixture_id': int           id api sport
        'tourn_id': int             id api sport
        'tourn_name':
        'tourn_short': str          nat_tournaments[ass][0]
        'season': YY-YY
        'tourn_round': str
        'club_nat':
        'club_TLpos':
        'club_qouta':               TL, UEFA, League, Cup
        'club_NATpos'
        'opp_nat':
        'opp_TLpos':
        'opp_qouta':
        'opp_NATpos':
        }
    ]
}
результат матча учитывается в standings, если:
    на момент начала матча оба играющих клуба находятся в списке участников
    основное время игры завершилось: только с 'game_status' = 'fixed'
расчет standings и формирование results по играм 'fixed'
формирование fixtures по играм 'unfinished' и 'expected'
'''

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    from modules.fixture_files import fixture_files
    from modules.add_game_main import add_game
    with open((os.path.abspath(__file__))[:-28]+'/cache/sub_results/participants_nat.json', 'r', encoding='utf-8') as j:
        participants = json.load(j)
    with open((os.path.abspath(__file__))[:-28]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
    dir_fixtures = os.listdir((os.path.abspath(__file__))[:-28]+'/cache/answers/fixtures')
    participants_id = []    # список id участников
    for ass in participants:
        for club in participants[ass]:
            participants_id.append(club['id'])

    # в games.json включать новые игры 'expected', начинающиеся позже последнего времени в worktimes.json, по рассчитанным участникам на месяц вперёд
    # извлечение времени последнего расчета
    with open((os.path.abspath(__file__))[:-28]+'/cache/sub_results/worktimes.json', 'r', encoding='utf-8') as j:
        worktimes = json.load(j)
    moment_timestamp = worktimes[-1][1]   # время момента расчета
    moment_datetime = worktimes[-1][0]
    # определение текущего сезона
    season = moment_datetime.year if moment_datetime.month > 7 else moment_datetime.year - 1
    season = str(season)[2:]+'-'+str(season+1)[2:]
    # поиск игр между участниками, начинающихся в течение месяца после момента расчета, по fixtures 
        # всех турниров UEFA и всех турниров нац ассоциаций с participants >1 (по participants_nat.json)
    # турниры UEFA
    from modules.int_tournaments import int_tournaments
    int_tournaments = int_tournaments()
    for ass in int_tournaments:
        for tourn in int_tournaments[ass]:
            # актуализация fixtures турнира
            if fixture_files(tourn[0], season, tourn[2]) == 'pass':     # если турнир не начался и нет расписания
                continue
            # открытие fixtures
            with open((os.path.abspath(__file__))[:-28]+'/cache/answers/fixtures/'+tourn[0]+' '+season+' fixt.json', 'r', encoding='utf-8') as j:
                fixtures = json.load(j)
            for match in fixtures['response']:
                if match['fixture']['timestamp'] > moment_timestamp and match['fixture']['timestamp'] < moment_timestamp + 3600*24*30 and\
                match['teams']['home']['id'] in participants_id and match['teams']['away']['id'] in participants_id:
                    if match['teams']['home']['id'] not in list(games.keys()):  # создание ключа
                        games[int(match['teams']['home']['id'])] = []
                    if match['teams']['away']['id'] not in list(games.keys()):  # создание ключа
                        games[int(match['teams']['away']['id'])] = []
                    # добавить игру в games
                    games[match['teams']['home']['id']].append(add_game(match, match['teams']['home']['id'], tourn[0], season))
                    games[match['teams']['away']['id']].append(add_game(match, match['teams']['away']['id'], tourn[0], season))
    # нац турниры
    from modules.nat_tournaments import Nat_Tournaments
    nat_tournaments = Nat_Tournaments()
    tourns = []     # список всех нац турниров [ENG League, id]
    for ass in participants:
        if len(participants[ass])>1:
            for nat_ass in nat_tournaments:
                if nat_ass == ass:
                    for tourn in nat_tournaments[nat_ass]:
                        if [tourn[0], tourn[3]] not in tourns and tourn[3] != -1:
                            tourns.append([tourn[0], tourn[3]])
    for tourn in tourns:
        # актуализация fixtures турнира
        if fixture_files(tourn[0], season, tourn[1]) == 'pass':     # если турнир не начался и нет расписания
            continue
        # открытие fixtures
        last_word = ' fixt' if 'League' in tourn[0] else ' curr'
        if tourn[0]+' '+season+last_word+'.json' not in dir_fixtures:
            continue
        with open((os.path.abspath(__file__))[:-28]+'/cache/answers/fixtures/'+tourn[0]+' '+season+last_word+'.json', 'r', encoding='utf-8') as j:
            fixtures = json.load(j)
        for match in fixtures['response']:
            if match['fixture']['timestamp'] > moment_timestamp and match['fixture']['timestamp'] < moment_timestamp + 3600*24*30 and\
            match['teams']['home']['id'] in participants_id and match['teams']['away']['id'] in participants_id:
                if match['teams']['home']['id'] not in list(games.keys()):  # создание ключа
                    games[match['teams']['home']['id']] = []
                if match['teams']['away']['id'] not in list(games.keys()):  # создание ключа
                    games[match['teams']['away']['id']] = []
                # добавить игру в games
                games[match['teams']['home']['id']].append(add_game(match, match['teams']['home']['id'], tourn[0], season))
                games[match['teams']['away']['id']].append(add_game(match, match['teams']['away']['id'], tourn[0], season))
    
    for club in games:
        # сортировка игр клуба от ранних к поздним
        games[club].sort(key=lambda match: match['timestamp'])

    # выгрузка games.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'games.json', games)
    runner_push(str(mod_name), 'sub_results', 'games.json', games)


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
