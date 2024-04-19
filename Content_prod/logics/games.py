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
        'tourn_nat_type': str       nat_tournaments[ass][0]
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
    # начавшиеся после предыдущего расчета (позже последнего времени в workflows.json):
        # 'fixed' - с завершенным основным временем
        # 'unfinished' - с незавершенным основным временем
            # если в них участвуют participants предыдущего расчета
            # нужен каталог /participants_history
            # после расчета записать текущее время в workflows.json
    # 'expected' - ожидаемые игры по текущему списку участников (для формирования fixtures)
        # могут исчезать и появлятся другие при изменении списка участников
        # на неделю вперед
# при каждом расчете 
    # из games.json проверять 'unfinished' на завершение основного времени и изменять их на 'fixed'
    # в games.json включать новые игры 'fixed' и 'unfinished', начавшиеся после предыдущего расчета 
        # (позже последнего времени в workflows.json до текущего времени):
    # из games.json удалять игры 'expected'
    # в games.json включать новые игры 'expected' по списку участников текущего расчета
# расчет standings и формирование results по играм 'fixed'
# формирование fixtures по играм 'unfinished' и 'expected'


try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    import os, json
    with open((os.path.abspath(__file__))[:-16]+'/cache/sub_results/participants.json', 'r', encoding='utf-8') as j:
        participants = json.load(j)
    with open((os.path.abspath(__file__))[:-16]+'/cache/sub_results/games.json', 'r', encoding='utf-8') as j:
        games = json.load(j)
    dir_fixtures = os.listdir((os.path.abspath(__file__))[:-16]+'/cache/answers/fixtures')

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
