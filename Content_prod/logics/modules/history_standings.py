# определение TL_standings на конкретную дату из каталога /standings_history
# возвращает содержимое файла json в виде словаря
# при ошибке - возвращает словарь с текущим TL_standings
def history_standings(hist_date):

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os, json
        # установить дату первого TL_standings в /standings_history
        use_standings_date = '2100-01-01'    # инициализация
        for standings_file in os.listdir((os.path.abspath(__file__))[:-36]+'/cache/sub_results/standings_history'):
            standings_date = standings_file[10:20]
            if 'standings' in standings_file and standings_date < use_standings_date:
                use_standings_date = standings_date
        # определение даты TL_standings, действовавших на момент hist_date
        for standings_file in os.listdir((os.path.abspath(__file__))[:-36]+'/cache/sub_results/standings_history'):
            standings_date = standings_file[10:20]
            if 'standings' in standings_file and standings_date < hist_date and standings_date > use_standings_date:
                use_standings_date = standings_date
        with open((os.path.abspath(__file__))[:-36]+'/cache/sub_results/standings_history/standings '\
            +str(use_standings_date)+'.json', 'r', encoding='utf-8') as j:
            hist_standings = json.load(j)

        return(hist_standings)

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
        
        # возврат текущий TL_standings
        import json
        with open((os.path.abspath(__file__))[:-36]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
            hist_standings = json.load(j)        
        return(hist_standings)