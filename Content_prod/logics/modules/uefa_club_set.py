def UEFA_club_set(october_year):   # определение текущего UEFA club set: 
                    # множества (удаление дубликатов) клубов из fixtures турниров за октябрь 2023 при запросе 01.09.23-31.08.24
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        import os   # импорт модуля работы с каталогами
        import time # модуль для паузы и определения текущего UEFA club set
        from modules.apisports_key import api_key   # модуль с ключом аккаунта api
        id_UEFA_Leagues = (2, 3, 848) # кортеж (неизменяемый список) id UEFA Leagues (UCL, UEL, UECL)
        
        # загрузка в папку cache api-запросов fixtures турниров за октябрь искомого года
        for id_league in id_UEFA_Leagues: # цикл по лигам УЕФА
            api_answer = api_key("/fixtures?league="+str(id_league)+"&season="+str(october_year)+
                                                    "&from="+str(october_year)+"-10-01&to="+str(october_year)+"-10-31")
            with open("cache\\"+str(id_league)+".txt", 'w') as f:
                f.write(api_answer)
            time.sleep(7)   # лимит: 10 запросов в минуту: между запросами 7 секунд: https://dashboard.api-football.com/faq Technical
        
        # набор UEFA club set из созданных файлов
        UEFA_clubs = [] # список клубов в UEFA club set
        for id_league in id_UEFA_Leagues: # цикл по лигам УЕФА
            with open("cache\\"+str(id_league)+".txt", 'r') as f:
                # проверка наличия fixtures в октябре: если хотя бы в одном из файлов не будет игр - использовать UEFA club set прошлого сезона 
                # проверка значения поля results
                for line in f:  # цикл по строкам
                    kursor = 0  # начальная позиция курсора
                    end_substr = 0   # позиция конца искомой подстроки
                    kursor = line.find('results":',0) +9    # переместить курсор перед искомой подстрокой
                    end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                    results = int(line[kursor:end_substr])  # извлечение значения поля results
                    if results == 0:    # если в файле нет игр
                        return("prev_season")   # использовать UEFA club set прошлого сезона
                # набор UEFA club set
                    while True:     # бесконечный цикл
                        if line.find('"teams"',kursor) ==-1:
                            break
                        kursor = line.find('"teams"',kursor)    # переместить курсор перед подстрокой "teams"
                        for х in range(1, 3):
                            kursor = line.find('"id":',kursor)+5    # переместить курсор за подстроку "id":
                            end_substr = line.find(',',kursor)    # определение конца искомой подстроки (поиск символа , после позиции курсора)
                            UEFA_club_id = line[kursor:end_substr]     # извлечение id клуба
                            kursor = line.find('"name":"',kursor)+8    # переместить курсор за подстроку "name":"
                            end_substr = line.find('"',kursor)    # определение конца искомой подстроки (поиск символа " после позиции курсора)
                            UEFA_club = line[kursor:end_substr]     # извлечение названия клуба
                            # UEFA_club = bytes(UEFA_club, "utf-8").decode("unicode_escape")   # декодирование символов не utf-8
                            # if UEFA_club.find("\\"): UEFA_club = UEFA_club.replace("\\","") # удаление из названия символов \\
                            if [UEFA_club, UEFA_club_id] not in UEFA_clubs:
                                UEFA_clubs.append([UEFA_club, UEFA_club_id])  # и добавление его в список

        # создание содержимого UEFA club set
        UefaClubSet_str = ''
        for club in range(0, len(UEFA_clubs)):
            if club == len(UEFA_clubs)-1: UefaClubSet_str += UEFA_clubs[club][0]+";   id:"+UEFA_clubs[club][1]+"."
            else: UefaClubSet_str += UEFA_clubs[club][0]+";   id:"+UEFA_clubs[club][1]+".\n"
        # выгрузка UEFA club set в репо (при неизмененном UEFA club set)
        mod_name = os.path.basename(__file__)[:-3]
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'club_sets', 'UefaClubSet_'+str(october_year)+'-'+str(october_year+1)+'.txt', UefaClubSet_str)
        # сохранение UEFA club set на текущем runner (для использования в текущем расчете сразу после его создания)
        with open((os.path.abspath(__file__))[:-35]+'/cache/sub_results/club_sets/\
            UefaClubSet_'+str(october_year)+'-'+str(october_year+1)+'.txt', 'w') as f:
            f.write(UefaClubSet_str)

        # # чистка папки cache
        # for id_league in id_UEFA_Leagues: # цикл по лигам УЕФА
        #     os.remove("cache\\"+str(id_league)+".txt")

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

        return("prev_season")   # приводит к использованию UEFA club set прошлого сезона