# жеребьевка группового этапа еврокубков проходит в конце августа
# для получения group set следует с 01.09 ежедневно делать запрос на игры в октябре, пока в папке club set/ не будет сформирован соответсвующий файл
# жеребьевка 1 стадии плей-офф еврокубков проходит на следующей неделе после 6-го тура групп в середине декабря. 1/16 проходит в феврале/марте
    # победители групп (до сезона 24/25) или 1-8 места общего этапа (с сезона 24/25) начинают с 1/8, жеребьевка которой проходит после 1/16
# для получения playoff set (до сезона 24/25) следует с 16.12 ежедневно делать запрос на игры в феврале и марте, 
    # пока в папке club set/ не будет сформирован соответсвующий файл
    # а также запрос standings на 1-е места групп для UEL и UECL, если запрос fixtures на февраль-март дал результат
# для получения playoff set (с сезона 24/25) с 01.02 запрашивать standings на 1-24 места в общем групповом этапе во всех трех турнирах 

def UEFAtournaments_club_set(tournament, season, stage):   # входящие параметры: турнир, сезон, стадия
    # список из множества (удаление дубликатов) клубов из fixtures турниров за необходимые месяцы

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        
        import os   # импорт модуля работы с каталогами
        import time # модуль для паузы и определения текущего UEFA club set
        from modules.apisports_key import api_key   # модуль с ключом аккаунта api
        os.mkdir('cache')   # создание временного каталога
        
        # определение id турнира
        if tournament == "UCL": id_league = 2
        elif tournament == "UEL": id_league = 3
        elif tournament == "UECL": id_league = 848

        # определение года начала сезона (для запроса)
        first_year = season[:4]
        
        if int(first_year) < 2024:    # до сезона 24/25

            # определение дат from-to
            if stage == "group set":
                from_to = "from="+str(season[:4])+"-10-01&to="+str(season[:4])+"-10-31"
            elif stage == "playoff set":
                from_to = "from="+str(season[5:])+"-02-01&to="+str(season[5:])+"-03-31"

            # загрузка в папку cache api-запросов fixtures турниров за октябрь (для групп) или февраль-март (для плейофф) искомого сезона
            api_answer = api_key("/fixtures?league="+str(id_league)+"&season="+str(first_year)+"&"+from_to)
            with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'w') as f:
                f.write(api_answer)
            time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical
            
            # набор tournament_club_set из созданного файла
            tournament_club_set = [] # список клубов турнира
            with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'r') as f:
                # проверка наличия fixtures: если в файле не будет игр - использовать предыдущий tournament_club_set
                # проверка значения поля results
                for line in f:  # цикл по строкам
                    kursor = 0  # начальная позиция курсора
                    end_substr = 0   # позиция конца искомой подстроки
                    kursor = line.find('results":',0) +9    # переместить курсор перед искомой подстрокой
                    end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                    results = int(line[kursor:end_substr])  # извлечение значения поля results
                    if results == 0:    # если в файле нет игр
                        return("use_prev")   # использовать предыдущий tournament_club_set
                # набор tournament_club_set
                    while True:     # бесконечный цикл
                        if line.find('"teams"',kursor) ==-1:
                            break
                        kursor = line.find('"teams"',kursor)    # переместить курсор перед подстрокой "teams"
                        for х in range(1, 3):
                            kursor = line.find('"id":',kursor)+5    # переместить курсор за подстроку "id":
                            end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                            tournament_club_id = line[kursor:end_substr]     # извлечение id клуба
                            kursor = line.find('"name":"',kursor)+8    # переместить курсор за подстроку "name":"
                            end_substr = line.find('"',kursor)    # определение конца искомой подстроки (поиск символа " после позиции курсора)
                            tournament_club = line[kursor:end_substr]     # извлечение названия клуба
                            if [tournament_club, tournament_club_id] not in tournament_club_set:
                                tournament_club_set.append([tournament_club, tournament_club_id])  # и добавление его в список

            # загрузка в папку cache api-запросов standings для определения 1-х мест групп (для UEL и UECL), тк они не попадают в fixtures запрос за февраль-март 
            if stage == "playoff set" and (tournament == "UEL" or tournament == "UECL"):
                api_answer = api_key("/standings?league="+str(id_league)+"&season="+str(first_year))
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'w') as f:
                    f.write(api_answer)
                time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical

                # добор 1-х мест групп (для UEL и UECL) в tournament_club_set из созданного файла
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'r') as f:
                    # проверка наличия standings: если в файле пусто - использовать предыдущий tournament_club_set
                    # проверка значения поля results
                    for line in f:  # цикл по строкам
                        kursor = 0  # начальная позиция курсора
                        end_substr = 0   # позиция конца искомой подстроки
                        kursor = line.find('results":',0) +9    # переместить курсор перед искомой подстрокой
                        end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                        results = int(line[kursor:end_substr])  # извлечение значения поля results
                        if results == 0:    # если в файле нет игр
                            return("use_prev")   # использовать предыдущий tournament_club_set
                    # набор tournament_club_set
                        while True:     # бесконечный цикл
                            if line.find('rank":1,"team":{"id":',kursor) ==-1:
                                break
                            kursor = line.find('rank":1,"team":{"id":',kursor)+21    # переместить курсор за подстроку rank":1,"team":{"id":
                            end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                            tournament_club_id = line[kursor:end_substr]     # извлечение id клуба
                            kursor = line.find('"name":"',kursor)+8    # переместить курсор за подстроку "name":"
                            end_substr = line.find('"',kursor)    # определение конца искомой подстроки (поиск символа " после позиции курсора)
                            tournament_club = line[kursor:end_substr]     # извлечение названия клуба
                            if [tournament_club, tournament_club_id] not in tournament_club_set:
                                tournament_club_set.append([tournament_club, tournament_club_id])  # и добавление его в список

        
        # с сезона 2024-2025: 
        elif int(first_year) > 2023:    # с сезона 24/25
        
            # определение дат from-to для group set
            if stage == "group set":
                from_to = "from="+str(season[:4])+"-10-01&to="+str(season[:4])+"-10-31"

            # загрузка в папку cache api-запросов fixtures турниров за октябрь (для групп) или standings на 1-24 места в общем групповом этапе (для плейофф)
            if stage == "group set":
                api_answer = api_key("/fixtures?league="+str(id_league)+"&season="+str(first_year)+"&"+from_to)
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'w') as f:
                    f.write(api_answer)
                time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical
            elif stage == "playoff set":
                api_answer = api_key("/standings?league="+str(id_league)+"&season="+str(first_year))
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'w') as f:
                    f.write(api_answer)
                time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical

            # набор tournament_club_set из созданного файла
            tournament_club_set = [] # список клубов турнира
            if stage == "group set":    # для групповой стадии добавляются все клубы из запроса
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'r') as f:
                    # проверка наличия fixtures: если в файле не будет игр - использовать предыдущий tournament_club_set
                    # проверка значения поля results
                    for line in f:  # цикл по строкам
                        kursor = 0  # начальная позиция курсора
                        end_substr = 0   # позиция конца искомой подстроки
                        kursor = line.find('results":',0) +9    # переместить курсор перед искомой подстрокой
                        end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                        results = int(line[kursor:end_substr])  # извлечение значения поля results
                        if results == 0:    # если в файле нет игр
                            return("use_prev")   # использовать предыдущий tournament_club_set
                    # набор tournament_club_set
                        while True:     
                            if line.find('"teams"',kursor) ==-1:
                                break
                            kursor = line.find('"teams"',kursor)    # переместить курсор перед подстрокой "teams"
                            for х in range(1, 3):
                                kursor = line.find('"id":',kursor)+5    # переместить курсор за подстроку "id":
                                end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                                tournament_club_id = line[kursor:end_substr]     # извлечение id клуба
                                kursor = line.find('"name":"',kursor)+8    # переместить курсор за подстроку "name":"
                                end_substr = line.find('"',kursor)    # определение конца искомой подстроки (поиск символа " после позиции курсора)
                                tournament_club = line[kursor:end_substr]     # извлечение названия клуба
                                if [tournament_club, tournament_club_id] not in tournament_club_set:
                                    tournament_club_set.append([tournament_club, tournament_club_id])  # и добавление его в список
            elif stage == "playoff set":    # для стадии плейофф 24 лучших клуба по итогам общей группы для всех турниров
                with open("cache\\"+tournament+" "+season+" "+stage+" request.txt", 'r') as f:
                    # проверка наличия standings: если в файле пусто - использовать предыдущий tournament_club_set
                    # проверка значения поля results
                    for line in f:  # цикл по строкам
                        kursor = 0  # начальная позиция курсора
                        end_substr = 0   # позиция конца искомой подстроки
                        kursor = line.find('results":',0) +9    # переместить курсор перед искомой подстрокой
                        end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                        results = int(line[kursor:end_substr])  # извлечение значения поля results
                        if results == 0:    # если в файле нет игр
                            return("use_prev")   # использовать предыдущий tournament_club_set
                    # набор tournament_club_set
                        rank = 1
                        while True:     # пока поиск не дошел до конца строки
                            if rank == 25:
                                break
                            if rank < 10:
                                len_substr = 21
                            else:
                                len_substr = 22
                            kursor = line.find('rank":'+str(rank)+',"team":{"id":',kursor) + len_substr    # переместить курсор за подстроку rank":...,"team":{"id":
                            end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                            tournament_club_id = line[kursor:end_substr]     # извлечение id клуба
                            kursor = line.find('"name":"',kursor)+8    # переместить курсор за подстроку "name":"
                            end_substr = line.find('"',kursor)    # определение конца искомой подстроки (поиск символа " после позиции курсора)
                            tournament_club = line[kursor:end_substr]     # извлечение названия клуба
                            if [tournament_club, tournament_club_id] not in tournament_club_set:
                                tournament_club_set.append([tournament_club, tournament_club_id])  # и добавление его в список
                            rank += 1
        
        # создание файла tournament_club_set в репо и на runner
        tournament_club_set_str = ''
        for club in range(0, len(tournament_club_set)):
            if club == len(tournament_club_set)-1:
                tournament_club_set_str += tournament_club_set[club][0]+";   id:"+tournament_club_set[club][1]+"."
            else:
                tournament_club_set_str += tournament_club_set[club][0]+";   id:"+tournament_club_set[club][1]+".\n"
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        from modules.runner_push import runner_push
        gh_push(str(mod_name), 'club_sets', tournament+" "+season+" "+stage+".txt", tournament_club_set_str)
        runner_push(str(mod_name), 'club_sets', tournament+" "+season+" "+stage+".txt", tournament_club_set_str)

        # чистка папки cache
        os.remove("cache\\"+tournament+" "+season+" "+stage+" request.txt")
        # удаление пустой папки cache
        os.rmdir('cache')

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

        return("use_prev")   # приводит к использованию предыдущего tournament_club_set