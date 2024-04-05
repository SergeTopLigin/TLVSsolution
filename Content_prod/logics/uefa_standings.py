try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # определение года в веб-адресе
    import datetime
    adress_year = datetime.datetime.utcnow()
    if adress_year.month < 9:
        adress_year = adress_year.year
    else:
        adress_year = adress_year.year +1

    from bs4 import BeautifulSoup
    import requests
    url = 'https://kassiesa.net/uefa/data/method5/trank'+str(adress_year)+'.html'
    response = requests.get(url)
    
    if str(response) != '<Response [200]>':     # создание файла ошибки с указанием файла кода и строки в нем
        message = \
            'uefa_standings\n'+\
            'ошибка при парсинге UEFA club ranking\n'+\
            'https://kassiesa.net/uefa/data/method5/trank'+str(adress_year)+'.html\n'+\
            'код ответа сервера != 200'
        # отправка bug_file в репозиторий GitHub и на почту
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'bug_files', 'bug_file', message)
        from modules.bug_mail import bug_mail
        bug_mail(str(mod_name), message)

    else:
        Page = str(BeautifulSoup(response.text,"html.parser"))
        # формирование словаря рейтинга УЕФА из html кода страницы
        UEFA50 = {}     # словарь рейтинга УЕФА {club:rate}
        kursor = 0      # начальная позиция поиска
        for num in range(0, 50):
            NameBegin = Page.find('>', Page.find('<td class="aleft', kursor)) +1
            NameEnd = Page.find('</td>', NameBegin)
            kursor = NameEnd
            club = Page[NameBegin : NameEnd]     # создание ключа словаря: имя клуба
            RateBegin = Page.find('<th class="lgray">', kursor) +18
            RateEnd = Page.find('</th>', RateBegin)
            kursor = RateEnd
            UEFA50[club] = Page[RateBegin : RateEnd]     # создание значения словаря: рейтинг клуба

        # преобразование имен клубов по apisports
        UEFA50upg = {}      # словарь измененных ключей
        DelUEFA = []        # список ключей словаря на удаление
        from modules.clubname_fix import clubname_fix  # модуль словаря {kassiesa:apifootball}
        converting = clubname_fix()
        for club in UEFA50:
            for club_fix in converting:
                if club == club_fix:
                    UEFA50upg[converting[club_fix]] = UEFA50[club]
                    DelUEFA.append(club)    # внесение неверных ключей словаря в словарь на удаление
        for club in DelUEFA:     # удаление исправленных
            del UEFA50[club] 
        for club in UEFA50upg:      # добавление исправленных
            UEFA50[club] = UEFA50upg[club]

        # если в словаре есть клуб несоответсвующий ни одному из имен в каталоге /standings - создать bug_file
        import os   # импорт модуля работы с каталогами
        import json
        dir_standings = os.listdir((os.path.abspath(__file__))[:-25]+'/cache/answers/standings')
        for club in UEFA50:
            find_club = 0
            for file in dir_standings:
                if 'json' in file:
                    with open((os.path.abspath(__file__))[:-25]+'/cache/answers/standings/'+file, 'r', encoding='utf-8') as f:
                        standings_dict = json.load(f)
                    for stage in standings_dict["response"][0]["league"]["standings"]:
                        for f_club in stage:
                            if f_club["team"]["name"] == club:
                                find_club = 1
                                break
                        if find_club == 1:
                            break
                    if find_club == 1:
                        break
            if find_club == 0:
                # отправка bug_file в репозиторий GitHub и на почту
                message = \
                    club+'   имя клуба не соответсвует apisports,'+\
                    ' внести в clubname_fix или добавить лигу в Content_prod/cache/answers/standings'
                import os
                mod_name = os.path.basename(__file__)[:-3]
                from modules.gh_push import gh_push
                gh_push(str(mod_name), 'bug_files', 'bug_file', message)
                from modules.bug_mail import bug_mail
                bug_mail(str(mod_name), message)

        # расчет TLstandings initial
        # (UEFA_club - UEFA_min) * (TL_max(2.2) - TL_min(-1.2)) / (UEFA_max - UEFA_min) - 1.2
        for club in UEFA50:
            UEFA50[club] = float(UEFA50[club])  # приведение строки к числу
        # определение макс и мин коэф в УЕФА топ50 
        UEFA_max = max(UEFA50.values())
        UEFA_min = min(UEFA50.values())
        for club in UEFA50:
            UEFA50[club] = round((UEFA50[club] - UEFA_min) * (2.2 - (-1.2)) / (UEFA_max - UEFA_min) - 1.2, 2)

        # сортировка TLstandings по убыванию: словаря по значению
        uefa_standings = dict(sorted(UEFA50.items(), key=lambda x: x[1], reverse=True))

        # приведение словаря uefa_standings к виду {club:[TL_rank,visual_rank]} 
        # с установкой визуально понятного рейтинга - в диапазоне 0-100 между 1-м и последним клубом
        TL_max = max(uefa_standings.values())
        TL_min = min(uefa_standings.values())
        for club in uefa_standings:
            TL_rank = uefa_standings[club]
            visual_rank = int(round(100 * (uefa_standings[club] - TL_min) / (TL_max - TL_min), 0))
            uefa_standings[club] = [TL_rank, visual_rank]
            
        # приведение словаря uefa_standings {club:[TL_rank,visual_rank]} 
        # к виду {club: {IDapi: , nat: , TL_rank: , visual_rank: }}
        # посредством \Content_prod\cache\answers\standings
        from modules.country_codes import country_codes
        country_codes = country_codes()
        uefa_standings_upg = {}
        for club in uefa_standings:
            find_club = 0
            for file in dir_standings:
                if 'json' in file and file[:3] in [nat['fifa'] for nat in country_codes]:
                    with open((os.path.abspath(__file__))[:-25]+'/cache/answers/standings/'+file, 'r', encoding='utf-8') as f:
                        standings_dict = json.load(f)
                    for stage in standings_dict["response"][0]["league"]["standings"]:
                        for f_club in stage:
                            if f_club["team"]["name"] == club:
                                uefa_standings_upg[club] = {'IDapi': f_club["team"]["id"], 'nat': file[:3], \
                                'TL_rank': uefa_standings[club][0], 'visual_rank': uefa_standings[club][1]}
                                find_club = 1
                                break
                        if find_club == 1:
                            break
                    if find_club == 1:
                        break

        # формирование .json из словаря TL-standings
        # и выгрузка uefa_standings.json в репо и на runner: /sub_results
        import json
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'sub_results', 'uefa_standings.json', uefa_standings_upg)
        from modules.runner_push import runner_push
        runner_push(str(mod_name), 'sub_results', 'uefa_standings.json', uefa_standings_upg)

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
