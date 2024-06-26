try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # определить UEFA club set > Content_prod\cache\sub_results\UEFA_club_sets\.json
    # проверка актуальности UEFA club set
    # в UEFA Club Set входят клубы, участвующие/участвовавшие в последней групповой стадии еврокубков, определяющиеся обычно к 01.09
    # для определения UEFA Club Set используется API запрос fixtures октября
    # определение имени необходимого файла
    # при запросе до 01.09 требуется файл, определенный октябрем прошлого года
    # при запросе после 31.08 требуется файл, определенный октябрем текущего года
    import datetime
    DateNow = datetime.datetime.utcnow()    # текущая дата по UTC
    if DateNow.month > 8:
        filename = "UefaClubSet_"+str(DateNow.year)+"-"+str(DateNow.year+1)
        october_year = DateNow.year
    else: 
        filename = "UefaClubSet_"+str(DateNow.year-1)+"-"+str(DateNow.year)
        october_year = DateNow.year-1
    # определить требуется ли API запрос или файл уже есть в базе
    create_flag = 1    # флаг необходимости создания файла
    import os
    for Set_file in os.listdir((os.path.abspath(__file__))[:-23]+'/cache/sub_results/club_sets'):
    # прочитать названия файлов из каталога club_sets
        if Set_file.find(filename)!=-1:  # если в каталоге club_set есть текущий UEFA Club Set
            create_flag = 0    # опустить флаг создания файла
            break
    if create_flag == 1:   # если флаг создания файла поднят - 
        # создать файл UEFA Club Set
        from modules.uefa_club_set import UEFA_club_set
        if UEFA_club_set(october_year) == "prev_season":   # или использовать UEFA club set прошлого сезона при ошибках
            filename = "UefaClubSet_"+str(DateNow.year-1)+"-"+str(DateNow.year)
    
    UefaClubSetID = []    # создание списка id из файла UefaClubSet
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/club_sets/'+filename+".txt", 'r') as f:
        for line in f:  # цикл по строкам
            kursor = line.find('id:',0) +3    # переместить курсор перед искомой подстрокой
            end_substr = line.find('.',kursor)    # определение конца искомой подстроки (поиск символа "." после позиции курсора)
            UefaClubSetID.append(int(line[kursor:end_substr]))

    # Association rating = total club set SUM(pts+1.2>=0) in TL standigs
    import json
    with open((os.path.abspath(__file__))[:-23]+'/cache/sub_results/final_standings.json', 'r', encoding='utf-8') as j:
        standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
    # определение UEFA rating
    UEFA_rating = 0
    for club in standings:
        for SetID in UefaClubSetID:
            if standings[club]['IDapi'] == SetID and standings[club]['buffer'] == False:
                UEFA_rating += max(standings[club]['TL_rank'] + 1.2, 0)
                break
    UEFA_rating = round(UEFA_rating, 2)
    # определение National ratings
    Nations_list = []    # создание списка национальных ассоциаций, имеющих представителство в TL standings
    Nations_list_rate = []  # и списка их рейтингов
    for club in standings:
        if standings[club]['buffer'] == False:
            Nations_list.append(standings[club]['nat'])
    Nations_list = list(set(Nations_list))  # избавляемся от повторных элементов преобразованием во множество и обратно
    for country in Nations_list:
        Nation_rate = 0   # инициализация рейтинга конкретной ассоциации
        for club in standings:
            if country == standings[club]['nat'] and standings[club]['buffer'] == False:
                Nation_rate += max(standings[club]['TL_rank'] + 1.2, 0)
        Nations_list_rate.append(round(Nation_rate, 2))
    # формирование общего словаря рейтингов ассоциаций
    Association_rating = dict(zip(Nations_list, Nations_list_rate))   # объединение списков нац ассоциаций и их рейтингов в одном словаре
    Association_rating["UEFA"] = UEFA_rating     # добавляем в словарь ассоциацию УЕФА

    # Association quota = ˻ 50 * Assoiation rating / Σ (Assoiation ratings) ˼
    Associations_rate_sum = 0   # сумма рейтингов ассоциаций
    for ass_n in Association_rating:
        Associations_rate_sum += Association_rating[ass_n]
    Associations_rate_sum = round(Associations_rate_sum, 2)
    import math
    for ass_n in Association_rating:
        Association_quota = max(math.floor(50 * Association_rating[ass_n] / Associations_rate_sum), 0)
        # увеличение вложенности словаря ассоциаций: {ass: {rating: ,quota: }}
        Association_rating[ass_n] = {'rating': Association_rating[ass_n], 'quota': Association_quota}
    # учет квоты TL на 10 лидеров
    # искусственное формирование рейтинга TL по пропорции рейтинга и квоты УЕФА
    TL_rating = round(10 * Association_rating["UEFA"]["rating"] / Association_rating["UEFA"]["quota"], 2)
    Association_rating["TopLiga"] = {'rating': TL_rating, 'quota': 10}

    # сортировка словаря рейтинга ассоциаций по убыванию рейтинга
    Association_rating = dict(sorted(Association_rating.items(), key=lambda x: x[1].get("rating"), reverse=True))   

    # формирование .json из словаря Association_rating
    # и выгрузка Association_rating.json в репо и на runner: /sub_results
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'sub_results', 'associations.json', Association_rating)
    from modules.runner_push import runner_push
    runner_push(str(mod_name), 'sub_results', 'associations.json', Association_rating)

    # формирование строки из словаря в читабельном виде
    from modules.country_codes import country_codes
    country_codes = country_codes()
    # github принимает только str для записи в файл
    ass_rate_quota_str = "{0:>23}  {1:}".format('quota', 'rating') + '\n'  # шапка таблицы
    rank = 1
    for ass in Association_rating:
        if Association_rating[ass]["quota"] > 0:
            if ass == "UEFA":       ass_name = "UEFA"
            elif ass == "TopLiga":  ass_name = "TopLiga"
            # изменение кодов стран на их имена
            else: ass_name = str([country_codes[country_codes.index(elem)]['name'] \
                for elem in country_codes if ass in elem['fifa']])[2:-2]
            ass_rate_quota_str += "{0:>2}  {1:15}  {3:>2}  {2:5.2f}"\
            .format(str(rank), ass_name, Association_rating[ass]["rating"], Association_rating[ass]["quota"])
            ass_rate_quota_str += '\n'
            rank += 1
    ass_rate_quota_str = ass_rate_quota_str[:-1]
    
    # выгрузка associations.txt в репо: /content и /content_commits  и на runner: /content
    gh_push(str(mod_name), 'content', 'associations.txt', ass_rate_quota_str)
    runner_push(str(mod_name), 'content', 'associations.txt', ass_rate_quota_str)
    gh_push(str(mod_name), 'content_commits', 'associations.txt', ass_rate_quota_str)

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
