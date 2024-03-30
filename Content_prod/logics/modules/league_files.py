# модуль актуализации файлов нац лиг по запросам fixtures и standings
# актуальные fixtures и standings применяются для: 
    # расчета рейтинга лиги: формирование club set на любой стадии посредством standings (в некоторых лигах проводится по несколько стадий)
    # определения участников от лиги
    # поиска матчей TL и их результатов посредством fixtures
# для актуализации standings необходим актуальный fixtures
# для актуализации fixtures следует делать запросы fixtures по окончании ближайшего несыгранного матча (не чаще)
# если по api запросу results != 0 - сохранить файл лиги, иначе - pass
def league_files(League, Season, LeagueID):     # League должен соответствовать названию турнира в Nat_tournaments.Nat_Tournaments[ass][0]
                                                                # Season = YY-YY (как в названии файла)
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        import json
        import datetime
        from modules.gh_push import gh_push
        from modules.runner_push import runner_push
        from modules.apisports_key import api_key    # модуль с ключом аккаунта api
        mod_name = os.path.basename(__file__)[:-3]
        from modules.bug_mail import bug_mail
        
        # проверка актуальности fixtures с возможным обновлением fixtures и standings
        find_fixtures = 0
        for League_file in os.listdir((os.path.abspath(__file__))[:-31]+'/cache/answers/fixtures/'):
            if League_file.find(League) != -1 and League_file.find(Season) != -1:
                with open((os.path.abspath(__file__))[:-31]+'/cache/answers/fixtures/'+League_file, 'r', encoding='utf-8') as f:
                    fixtures_dict = json.load(f)
                # если наступило время окончания следующего несыгранного матча и сезон не закончился - обновить fixtures
                time_now = datetime.datetime.utcnow()    # текущее время UTC
                # определение окончания самого раннего матча при status short in [NS, 1H, HT, 2H, INT]
                next_match_time = 4000000000
                for match in fixtures_dict['response']:
                    if (match['fixture']['status']['short'] in ['NS', '1H', 'HT', '2H', 'INT']) and (match['fixture']['timestamp'] < next_match_time):
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
                file_name = League+" "+Season+" fixt.json"
                gh_push(str(mod_name), 'fixtures', file_name, answer_dict)
                runner_push(str(mod_name), 'fixtures', file_name, answer_dict)
            else:
                gh_push(str(mod_name), 'bug_files', 'bug_file', "по запросу fixtures?league="+str(LeagueID)+"&season="+FixtSeason+" results=0")
                bug_mail(str(mod_name), "по запросу fixtures?league="+str(LeagueID)+"&season="+FixtSeason+" results=0")
            answer = api_key("/standings?league="+str(LeagueID)+"&season="+FixtSeason)
            # если 'results' != 0 - сохранить standings
            answer_dict = json.loads(answer)
            if answer_dict['results'] != 0:
                file_name = League+" "+Season+" stan.json"
                gh_push(str(mod_name), 'standings', file_name, answer_dict)
                runner_push(str(mod_name), 'standings', file_name, answer_dict)
            else:
                gh_push(str(mod_name), 'bug_files', 'bug_file', "по запросу standings?league="+str(LeagueID)+"&season="+FixtSeason+" results=0")
                bug_mail(str(mod_name), "по запросу standings?league="+str(LeagueID)+"&season="+FixtSeason+" results=0")

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
