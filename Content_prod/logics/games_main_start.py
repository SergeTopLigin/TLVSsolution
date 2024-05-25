'''
функция games_main_start.py:
- фиксация момента расчета в worktimes.json
- определение результатов игр unfinished и expected, завершившихся до момента расчета, перевод их в статус fixed
- перевод начавшихся до момента расчета и незаконченных игр из expected в unfinished
- удаление оставшихся игр expected


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

    import os, json, time, datetime
    from modules.gh_push import gh_push
    from modules.runner_push import runner_push
    mod_name = os.path.basename(__file__)[:-3]
    dir_fixtures = os.listdir((os.path.abspath(__file__))[:-27]+'/cache/answers/fixtures')
    from modules.apisports_key import api_key


    # фиксация момента расчета в worktimes.json
    curr_timestamp = time.time()
    curr_datetime = datetime.datetime.utcnow()
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/worktimes.json', 'r', encoding='utf-8') as j:
        worktimes = json.load(j)
    worktimes.append([str(curr_datetime), curr_timestamp])
    # и выгрузка worktimes.json в репо и на runner: /sub_results
    gh_push(str(mod_name), 'sub_results', 'worktimes.json', worktimes)
    runner_push(str(mod_name), 'sub_results', 'worktimes.json', worktimes)


    # определение результатов игр unfinished и expected, завершившихся до момента расчета, перевод их в статус fixed
    # перевод начавшихся до момента расчета и незаконченных игр из expected в unfinished
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
    # список id игр unfinished и expected, начавшихся до момента расчета
    new_fixed = []  
    for club_id in games:
        for game in games[club_id]:
            if game['game_status'] in ['unfinished', 'expected'] and curr_timestamp > game['timestamp']:
                new_fixed.append(str(game['fixture_id']))
    # список запросов: макс 20 ids в одном запросе
    requests = []    
    for fixture in new_fixed:
        n = new_fixed.index(fixture) // 20   # индекс списка requests - номер запроса
        if len(requests) < n+1:
            requests.append(fixture)
        else:
            requests[n] += '-'+fixture
    # запросы результатов игр и изменение games.json
    reg_time = ['ET', 'BT', 'P', 'FT', 'AET', 'PEN']    # статусы окончания основного времени
    play_time = ['1H', 'HT', '2H', 'LIVE']      # статусы незаконченного основного времени
    for request in requests:
        response = api_key("/fixtures?ids="+request)
        time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical
        response_dict = json.loads(response)
        if response_dict['results'] != 0:
            # определение результатов игр unfinished и expected, завершившихся до момента расчета, перевод их в статус fixed
            for fixture in [fixt for fixt in response_dict['response'] if fixt['fixture']['status']['short'] in reg_time or \
            (fixt['fixture']['status']['short'] in ['SUSP', 'INT'] and fixt['fixture']['status']['elapsed'] >= 90)]:
                for club_id in [cl_id for cl_id in games if int(cl_id) in [fixture['teams']['home']['id'], fixture['teams']['away']['id']]]:
                    for game in [g for g in games[club_id] if g['fixture_id'] == fixture['fixture']['id']]:
                        game['game_status'] = 'fixed'
                        game['match'] = fixture['teams']['home']['name']+' - '+fixture['teams']['away']['name']+'   '+\
                            str(fixture['score']['fulltime']['home'])+':'+str(fixture['score']['fulltime']['away'])
                        # result
                        if (int(club_id) == fixture['teams']['home']['id'] and fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away'])\
                        or (int(club_id) == fixture['teams']['away']['id'] and fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away']):
                            game['result'] = 'win'
                        elif (int(club_id) == fixture['teams']['home']['id'] and fixture['score']['fulltime']['home'] < fixture['score']['fulltime']['away'])\
                        or (int(club_id) == fixture['teams']['away']['id'] and fixture['score']['fulltime']['home'] > fixture['score']['fulltime']['away']):
                            game['result'] = 'lose'
                        elif fixture['score']['fulltime']['home'] == fixture['score']['fulltime']['away']:
                            game['result'] = 'draw'
                        # goalDiff
                        if int(club_id) == fixture['teams']['home']['id']:
                            game['goalDiff'] = fixture['score']['fulltime']['home'] - fixture['score']['fulltime']['away']
                        if int(club_id) == fixture['teams']['away']['id']:
                            game['goalDiff'] = fixture['score']['fulltime']['away'] - fixture['score']['fulltime']['home']
            # перевод начавшихся до момента расчета и незаконченных игр из expected в unfinished
            for fixture in [fixt for fixt in response_dict['response'] if fixt['fixture']['status']['short'] in play_time or \
            (fixt['fixture']['status']['short'] in ['SUSP', 'INT'] and fixt['fixture']['status']['elapsed'] < 90)]:
                for club_id in [cl_id for cl_id in games if int(cl_id) in [fixture['teams']['home']['id'], fixture['teams']['away']['id']]]:
                    for game in [g for g in games[club_id] if g['fixture_id'] == fixture['fixture']['id']]:
                        game['game_status'] = 'unfinished'

    
    # удаление оставшихся игр expected
    del_club = []
    for club_id in games:
        new_game_set = []
        for game in games[club_id]:
            if game['game_status'] != 'expected':
                new_game_set.append(game)
        games[club_id] = new_game_set

    # удаление клубов без игр
        if len(games[club_id]) == 0:
            del_club.append(club_id)
    for club in del_club:
        games.pop(club)


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
