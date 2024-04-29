# игры хранятся в словаре {club: [games{}]}
# в список по ключу клуба попадает каждая игра этого клуба в рамках TL
# каждая игра это словарь, включающий ключи: соперник, дата, счет, рейтинг соперника на момент игры и др характеристики для расчета standings клуба
'''
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
'''

# результат матча учитывается в standings, если:
    # на момент начала матча оба играющих клуба находятся в списке участников
    # основное время игры завершилось: только с 'game_status' = 'fixed'
# в словарь games.json занести игры, 
    # начавшиеся после предыдущего расчета (позже последнего времени в worktimes.json):
        # 'fixed' - с завершенным основным временем
        # 'unfinished' - с незавершенным основным временем
    # 'expected' - ожидаемые игры по текущему списку участников (для формирования fixtures)
        # могут исчезать и появлятся другие при изменении списка участников
        # на месяц вперед
# при каждом расчете 
    # из games.json проверять 'unfinished' на завершение основного времени и изменять их на 'fixed'
    # в games.json включать новые игры 'fixed' и 'unfinished', начавшиеся после предыдущего расчета 
        # (позже последнего времени в worktimes.json до текущего времени):
    # из games.json удалять игры 'expected'
    # в games.json включать новые игры 'expected' по списку участников текущего расчета
    # после расчета записать текущее время в worktimes.json
# расчет standings и формирование results по играм 'fixed'
# формирование fixtures по играм 'unfinished' и 'expected'


try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json, time, datetime
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    from modules.fixture_files import fixture_files
    from modules.add_game import add_game
    with open((os.path.abspath(__file__))[:-16]+'/cache/sub_results/participants_nat.json', 'r', encoding='utf-8') as j:
        participants = json.load(j)
    with open((os.path.abspath(__file__))[:-16]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
    dir_fixtures = os.listdir((os.path.abspath(__file__))[:-16]+'/cache/answers/fixtures')
    participants_id = []    # список id участников
    for ass in participants:
        for club in participants[ass]:
            participants_id.append(club['id'])

    # из games.json удалить игры 'expected'
    for club_id in games:
        new_game_set = []
        for game in games[club_id]:
            if game['game_status'] != 'expected':
                new_game_set.append(game)
        games[club_id] = new_game_set
    
    # из games.json проверять 'unfinished' на завершение основного времени и изменять их на 'fixed'
    for club_id in games:
        for game in games[club_id]:
            if game['game_status'] == 'unfinished':
                fixt_file = [file for file in dir_fixtures if game['tourn_nat_type'] in file and game['season'] in file][0]
                with open((os.path.abspath(__file__))[:-16]+'/cache/answers/fixtures'+fixt_file, 'r', encoding='utf-8') as j:
                    tourn_fixtures = json.load(j)
                for fixture in tourn_fixtures['response']:
                    if game['fixture_id'] == fixture['fixture']['id'] and \
                    fixture['fixture']['status']['short'] in ['ET', 'BT', 'P', 'FT', 'AET', 'PEN']:
                        game['game_status'] = 'fixed'
                        game['match'] = fixture['teams']['home']['name']+' - '+fixture['teams']['away']['name']+'   '+\
                            fixture['score']['fulltime']['home']+':'+fixture['score']['fulltime']['away']
                        # result
                        if (club_id == fixture['teams']['home']['id'] and fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away'])\
                        or (club_id == fixture['teams']['away']['id'] and fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away']):
                            game['result'] = 'win'
                        elif (club_id == fixture['teams']['home']['id'] and fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away'])\
                        or (club_id == fixture['teams']['away']['id'] and fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away']):
                            game['result'] = 'lose'
                        elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:
                            game['result'] = 'draw'
                        # goalDiff
                        if club_id == fixture['teams']['home']['id']:
                            game['goalDiff'] = fixture['score']['fulltime']['home'] - fixture['score']['fulltime']['away']
                        if club_id == fixture['teams']['away']['id']:
                            game['goalDiff'] = fixture['score']['fulltime']['away'] - fixture['score']['fulltime']['home']
                        break
                    if game['fixture_id'] == fixture['fixture']['id']:
                        break

    # в games.json включать новые игры 'fixed' и 'unfinished', начавшиеся после предыдущего расчета 
        # (позже последнего времени в worktimes.json до текущего времени):
    # в games.json включать новые игры 'expected' по списку участников текущего расчета на месяц вперёд
    # определение текущего времени
    curr_timestamp = time.time()
    curr_datetime = datetime.datetime.utcnow()
    # извлечение времени последнего расчета
    with open((os.path.abspath(__file__))[:-16]+'/cache/sub_results/worktimes.json', 'r', encoding='utf-8') as j:
        worktimes = json.load(j)
    # если worktimes.json пуст - новые игры 'fixed' и 'unfinished' не включаются до следующего расчета
    if len(worktimes) > 0:
        prev_timestamp = worktimes[-1][1]   # время предыдущего расчета
        # определение текущего сезона
        season = curr_datetime.year if curr_datetime.month > 7 else curr_datetime.year - 1
        season = str(season)[2:]+'-'+str(season+1)[2:]
        # поиск игр между участниками, начавшихся между prev_timestamp и curr_timestamp, по fixtures 
            # всех турниров UEFA и всех турниров нац ассоциаций с participants >1 (по participants_nat.json)
        # турниры UEFA
        from modules.int_tournaments import int_tournaments
        int_tournaments = int_tournaments()
        for ass in int_tournaments:
            for tourn in ass:
                # актуализация fixtures турнира
                if fixture_files(tourn[0], season, tourn[2]) == 'pass':     # если турнир не начался и нет расписания
                    continue
                # открытие fixtures
                with open((os.path.abspath(__file__))[:-16]+'/cache/answers/fixtures/'+tourn[0]+' '+season+' fixt.json', 'r', encoding='utf-8') as j:
                    fixtures = json.load(j)
                for match in fixtures['response']:
                    if match['fixture']['timestamp'] > prev_timestamp and match['fixture']['timestamp'] < curr_timestamp + 2500000 and\
                    match['teams']['home']['id'] in participants_id and match['teams']['away']['id'] in participants_id:
                        if match['teams']['home']['id'] not in list(games.keys()):  # создание ключа
                            games[match['teams']['home']['id']] = []
                        if match['teams']['away']['id'] not in list(games.keys()):  # создание ключа
                            games[match['teams']['away']['id']] = []
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
            with open((os.path.abspath(__file__))[:-16]+'/cache/answers/fixtures/'+tourn[0]+' '+season+last_word+'.json', 'r', encoding='utf-8') as j:
                fixtures = json.load(j)
            for match in fixtures['response']:
                if match['fixture']['timestamp'] > prev_timestamp and match['fixture']['timestamp'] < curr_timestamp + 2500000 and\
                match['teams']['home']['id'] in participants_id and match['teams']['away']['id'] in participants_id:
                    if match['teams']['home']['id'] not in list(games.keys()):  # создание ключа
                        games[match['teams']['home']['id']] = []
                    if match['teams']['away']['id'] not in list(games.keys()):  # создание ключа
                        games[match['teams']['away']['id']] = []
                    # добавить игру в games
                    games[match['teams']['home']['id']].append(add_game(match, match['teams']['home']['id'], tourn[0], season))
                    games[match['teams']['away']['id']].append(add_game(match, match['teams']['away']['id'], tourn[0], season))
    # фиксация в worktimes.json времени текущего расчета
    worktimes.append([curr_datetime, curr_timestamp])
    # и выгрузка worktimes.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'worktimes.json', worktimes)
    runner_push(str(mod_name), 'sub_results', 'worktimes.json', worktimes)


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
