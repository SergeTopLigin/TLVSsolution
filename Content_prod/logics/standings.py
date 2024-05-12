# формирование standings
# uefa_standings.py > sub_result/uefa_standings.json
# TL_standings.py > sub_result/TL_standings.json
# standings.py > sub_result/final_standings.json, content/standings.txt, content-commits/standings.txt
# для объединения uefa_standings и TL_standings в final_standings временно прибавить к рейтингам клубов в обоих standings по +5
    # это выведет в + даже самое крупное недавнее поражение в TL

try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

    # определение влияния UEFA club rankings на текущий TL standings
    import datetime
    # TL_start_date: 100% UEFA club rankings + 0% TL standings
    TL_start_date = datetime.datetime(2025, 1, 1)   # дата начала обработки игр TL
    # каждый следующий день в 0:00 1/365 переходит в standings
    # определение количества полных дней после TL_start_date по UTC
    if datetime.datetime.utcnow() <= TL_start_date:
        Days_after_start = 0
    elif datetime.datetime.utcnow() > TL_start_date + datetime.timedelta(days=365):
        Days_after_start = 365
    else: 
        Days_after_start = min(int((datetime.datetime.utcnow()-TL_start_date)//datetime.timedelta(days=1)), 365)
    # коэффициент влияния rate TL standings на итоговый rate клубов
    TL_Influence = (1/365)*Days_after_start
    # коэффициент влияния UEFA club rankings на итоговый rate клубов
    UEFA_Influence = 1-TL_Influence

    # формирование исходных uefa_standings и TL_standings при необходимости
    import json
    import os
    if TL_Influence > 0:
        # декодирование из файла TL_standings
        with open((os.path.abspath(__file__))[:-20]+'/cache/sub_results/TL_standings.json', 'r', encoding='utf-8') as j:
            TL_standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
    if UEFA_Influence > 0:
        # декодирование из файла uefa_standings
        with open((os.path.abspath(__file__))[:-20]+'/cache/sub_results/uefa_standings.json', 'r', encoding='utf-8') as j:
            uefa_standings = json.load(j)   # {club: {IDapi: , nat: , TL_rank: , visual_rank: }}
        
    # формирование словаря final_standings
    if UEFA_Influence == 1:
        final_standings = uefa_standings
    elif TL_Influence == 1:
        final_standings = TL_standings
    else:   # объединение uefa_standings и TL_standings
        final_standings = {}
        # объединить клубы из обоих словарей
        final_standings_list = list(uefa_standings.keys()) + list(TL_standings.keys())  # список клубов обоих standings
        final_standings_list = list(set(final_standings_list))  # убрать повторы через множество
        for club in final_standings_list:
            if club in TL_standings and club in uefa_standings:
                final_standings[club] = TL_standings[club]
                final_standings[club]['TL_rank'] = \
                (TL_standings[club]['TL_rank']+5)*TL_Influence + (uefa_standings[club]['TL_rank']+5)*UEFA_Influence - 5
            elif club in TL_standings:
                final_standings[club] = TL_standings[club]
                final_standings[club]['TL_rank'] = (TL_standings[club]['TL_rank']+5)*TL_Influence - 5
            elif club in uefa_standings:
                final_standings[club] = uefa_standings[club]
                final_standings[club]['TL_rank'] = (uefa_standings[club]['TL_rank']+5)*UEFA_Influence - 5
                final_standings[club]['played'] = 0
        # visual_rank
        TL_rank_max = max([final_standings[club]['TL_rank'] for club in final_standings])
        TL_rank_min = min([final_standings[club]['TL_rank'] for club in final_standings])
        for club in final_standings:
            final_standings[club]['visual_rank'] = int(round(100 * (final_standings[club]['TL_rank'] - TL_rank_min) / (TL_rank_max - TL_rank_min), 0))
        # сортировка TL_standings с учетом buffer: 
        # в main_stands попадают:
        # в первые 122 дня после TL_start_date - все клубы
        # с 123 по 244 день после TL_start_date - клубы, сыгравшие 1 игру
        # с 245 по 365 день после TL_start_date - клубы, сыгравшие 2 игры
        main_stands = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] > 2}
        main_stands = dict(sorted(main_stands.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        # в buffer_2pl попадают клубы, сыгравшие 2 игры
        buffer_2pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] == 2}
        buffer_2pl = dict(sorted(buffer_2pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        # в buffer_1pl попадают клубы, сыгравшие 1 игру
        buffer_1pl = {club:TL_standings[club] for club in TL_standings if TL_standings[club]['played'] == 1}
        buffer_1pl = dict(sorted(buffer_1pl.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))
        # переинициализация TL-standings
        TL_standings = {}
        for club in main_stands:
            TL_standings[club] = main_stands[club]
        for club in buffer_2pl:
            TL_standings[club] = buffer_2pl[club]
        for club in buffer_1pl:
            TL_standings[club] = buffer_1pl[club]

    
    # формирование .json из словаря final_standings
    # и выгрузка final_standings.json в репо и на runner: /sub_results
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'sub_results', 'final_standings.json', final_standings)
    gh_push(str(mod_name), 'standings_history', 'standings.json', final_standings)
    from modules.runner_push import runner_push
    runner_push(str(mod_name), 'sub_results', 'final_standings.json', final_standings)

    # формирование строки из словаря в читабельном виде
    final_standings_str = ''   # github принимает только str для записи в файл
    rank = 1
    for club in final_standings:
        final_standings_str += "{0:>2}  {1:25}{2:3.0f}   {3:5.2f}    {4}".\
        format(str(rank), club, final_standings[club]['visual_rank'], final_standings[club]['TL_rank'], \
            final_standings[club]['nat']) + '\n'
        rank += 1

    # выгрузка standings.txt в репо: /content и /content_commits  и на runner: /content
    gh_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
    runner_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
    gh_push(str(mod_name), 'content_commits', 'standings.txt', final_standings_str)

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
