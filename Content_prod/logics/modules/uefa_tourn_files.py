# модуль актуализации файлов турниров УЕФА по запросам fixtures и standings
# актуальные fixtures и standings применяются для: 
    # определения участников от турнира
    # поиска матчей TL и их результатов посредством fixtures
# для актуализации standings на групповой стадии необходим актуальный fixtures
# для актуализации fixtures следует делать запросы fixtures по окончании ближайшего несыгранного матча (не чаще)
# если по api запросу results != 0 - сохранить файл лиги, иначе - pass
def uefa_tourn_files(Tourn, Season, LeagueID, Stage):     # Tourn должен соответствовать названию турнира в ("UCL", "UEL", "UECL")
                                                                # Season = YY-YY (как в названии файла)
                                                                # Stage = 'group' / 'playoff'
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        import json
        import datetime
        from modules.gh_push import gh_push
        from modules.runner_push import runner_push
        from modules.apisports_key import api_key    # модуль с ключом аккаунта api

        # проверка актуальности fixtures с возможным обновлением fixtures и standings
        find_fixtures = 0
        for League_file in os.listdir((os.path.abspath(__file__))[:-35]+'/cache/answers/fixtures/'):
            if League_file.find(Tourn) != -1 and League_file.find(Season) != -1:
                with open((os.path.abspath(__file__))[:-35]+'/cache/answers/fixtures/'+League_file, 'r', encoding='utf-8') as f:
                    fixtures_dict = json.load(f)
                # если наступило время окончания следующего несыгранного матча и сезон не закончен - обновить fixtures
                time_now = datetime.datetime.utcnow()    # текущее время UTC
                # определение окончания самого раннего матча при status short in ['NS', '1H', 'HT', '2H', 'ET', 'BT', 'P', 'INT']
                next_match_time = 4000000000
                for match in fixtures_dict['response']:
                    if (match['fixture']['status']['short'] in ['NS', '1H', 'HT', '2H', 'ET', 'BT', 'P', 'INT']) \
                    and (match['fixture']['timestamp'] < next_match_time):
                        next_match_time = match['fixture']['timestamp']
                next_match_time += 8000
                if time_now < datetime.datetime.utcfromtimestamp(next_match_time) or next_match_time > 4000000000:
                    find_fixtures = 1

        # если fixtures турнира нет или время окончания ближайшего несыгранного матча пришло
        if find_fixtures == 0:   # запрос fixtures и standings
            FixtSeason = "20"+Season[:2]
            answer = api_key("/fixtures?league="+str(LeagueID)+"&season="+FixtSeason)
            # если 'results' != 0 - сохранить fixtures
            answer_dict = json.loads(answer)
            if answer_dict['results'] != 0:
                mod_name = os.path.basename(__file__)[:-3]
                file_name = Tourn+" "+Season+" fixt.json"
                gh_push(str(mod_name), 'fixtures', file_name, answer_dict)
                runner_push(str(mod_name), 'fixtures', file_name, answer_dict)
            
            # если вызов из групповой стадии - обновить standings
            if Stage == 'group':
            answer = api_key("/standings?league="+str(LeagueID)+"&season="+FixtSeason)
            # если 'results' != 0 - сохранить standings
            answer_dict = json.loads(answer)
            if answer_dict['results'] != 0:
                mod_name = os.path.basename(__file__)[:-3]
                file_name = Tourn+" "+Season+" stan.json"
                gh_push(str(mod_name), 'standings', file_name, answer_dict)
                runner_push(str(mod_name), 'standings', file_name, answer_dict)

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

        return("pass")     # приводит к ожиданию следующего workflow для перерасчета этой лиги
