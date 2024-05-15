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
    from modules.add_game import add_game
    dir_fixtures = os.listdir((os.path.abspath(__file__))[:-27]+'/cache/answers/fixtures')


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
    with open((os.path.abspath(__file__))[:-27]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
# fixtures?ids=id-id-id (max 20 за запрос)
    new_fixed = []  # список id игр unfinished и expected, завершившихся до момента расчета
    for club_id in games:
        for game in games[club_id]:
            if game['game_status'] in ['unfinished', 'expected'] and curr_timestamp > game['timestamp'] + 115*60:
                new_fixed.append(str(game['fixture_id']))




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
