'''
модуль формирует из игры списка fixtures['response'] словарь вида:
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
для включения его в словарь games
'''

def add_game(fixture, club_id):     # fixture - словарь из списка fixtures['response']
                                    # club_id - ключ словаря games, в список значения которого следует добавить игру
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except



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
