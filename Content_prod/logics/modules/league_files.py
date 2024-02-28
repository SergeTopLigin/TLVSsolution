# модуль актуализации файлов нац лиг по запросу fixtures для определения club set
# если по api запросу results != 0 - сохранить файл лиги, иначе - pass
def set_league_files(League, Season, LeagueID):     # League должен соответствовать названию турнира в mod_Nat_tournaments.Nat_Tournaments[ass][0]
                                                                # Season = YY-YY (как в названии файла)
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        from modules.gh_push import gh_push
        from modules.runner_push import runner_push
        for League_file in os.listdir((os.path.abspath(__file__))[:-31]+'/cache/answers/fixtures/'):
            if League_file.find(League) != -1 and League_file.find(Season) != -1:
                return("pass")
        from modules.apisports_key import api_key    # модуль с ключом аккаунта api
        FixtSeason = "20"+Season[:2]
        api_league = api_key("/fixtures?league="+LeagueID+"&season="+FixtSeason)
        mod_name = os.path.basename(__file__)[:-3]
        file_name = League+" "+Season+".json"
        gh_push(str(mod_name), 'fixtures', file_name, api_league)
        runner_push(str(mod_name), 'fixtures', file_name, api_league)

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