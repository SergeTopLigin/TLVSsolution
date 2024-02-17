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
            'init_standings\n'+\
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
        dir_standings = os.listdir((os.path.abspath(__file__))[:-25]+'/cache/answers/standings')
        for club in UEFA50:
            find_club = 0
            for file in dir_standings:
                with open((os.path.abspath(__file__))[:-25]+'/cache/answers/standings/'+file, 'r') as f:
                    for line in f:  # цикл по строкам
                        end_substr = 0
                        while True:     # бесконечный цикл
                            if line.find('name":"',end_substr) ==-1:
                                break
                            kursor = line.find('name":"',end_substr) +7    # переместить курсор перед искомой подстрокой
                            end_substr = line.find('","',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
                            if club == line[kursor:end_substr]:
                                find_club = 1
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
        TL_standings = dict(sorted(UEFA50.items(), key=lambda x: x[1], reverse=True))

        # приведение словаря TL_standings к виду {club:[TL_rank,visual_rank]} 
        # с установкой визуально понятного рейтинга - в диапазоне 0-100 между 1-м и последним клубом
        TL_max = max(TL_standings.values())
        TL_min = min(TL_standings.values())
        for club in TL_standings:
            TL_rank = TL_standings[club]
            visual_rank = int(round(100 * (TL_standings[club] - TL_min) / (TL_max - TL_min), 0))
            TL_standings[club] = [TL_rank, visual_rank]
            
        # формирование .json из словаря TL-standings
        # и выгрузка init_standings.json в репо: /sub_results
        import json
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'sub_results', 'init_standings.json', \
            json.dumps(TL_standings, skipkeys=True, ensure_ascii=False, indent=2))

        # # формирование строки из словаря в читабельном виде
        # TL_standings_str = ''   # github принимает только str для записи в файл
        # rank = 1
        # for club in TL_standings:
        #     TL_standings_str += "{3:>2}  {0:20}   {2:3.0f}   {1:5.2f}".\
        #     format(club, TL_standings[club][0], TL_standings[club][1], str(rank)) + '\n'
        #     rank += 1
        # # # формирование в конце строки списка для передачи в дальнейшие расчеты
        # # TL_standings_str += '\noutput list['
        # # for club in TL_standings:
        # #     TL_standings_str += r'["'+club+r'", '+str(TL_standings[club][0])+', '+str(TL_standings[club][1])+'],'
        # # TL_standings_str = TL_standings_str[:-1] + ']'      # удаление последней запятой

        # # выгрузка standings.txt в репо: /content и /content_commits
        # import os
        # mod_name = os.path.basename(__file__)[:-3]
        # from modules.gh_push import gh_push
        # gh_push(str(mod_name), 'content', 'standings.txt', TL_standings_str)
        # gh_push(str(mod_name), 'content_commits', 'standings.txt', TL_standings_str)

        # # for club in TL_standings:
        # #     print(club,'   ',TL_standings[club])

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
