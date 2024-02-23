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
        Days_after_start = int((datetime.datetime.utcnow()-TL_start_date)//datetime.timedelta(days=1))
    # коэффициент влияния rate TL standings на итоговый rate клубов
    TL_Influence = (1/365)*Days_after_start
    # коэффициент влияния UEFA club rankings на итоговый rate клубов
    UEFA_Influence = 1-TL_Influence

    # формирование исходных uefa_standings и TL_standings при необходимости
    import json
    import os
    if TL_Influence > 0:
        # декодирование из файла TL_standings
        with open((os.path.abspath(__file__))[:-20]+'/cache/sub_results/TL_standings.json', 'r') as j:
            TL_standings = json.load(j) # {club: {IDapi: , nat: , TL_rank: , visual_rank: }} 
    if UEFA_Influence > 0:
        # декодирование из файла uefa_standings
        with open((os.path.abspath(__file__))[:-20]+'/cache/sub_results/uefa_standings.json', 'r') as j:
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

    # установка визуально понятного рейтинга - в диапазоне 0-100 между 1-м и последним клубом
    max_rank = -10
    min_rank = 10
    for club in final_standings:
        if final_standings[club]['TL_rank'] > max_rank:
            max_rank = final_standings[club]['TL_rank']
        if final_standings[club]['TL_rank'] < min_rank:
            min_rank = final_standings[club]['TL_rank']
    for club in final_standings:
        visual_rank = int(round(100 * (final_standings[club]['TL_rank'] - min_rank) / (max_rank - min_rank), 0))
        final_standings[club]['visual_rank'] = visual_rank

    # сортировка final_standings по TL_rank
    final_standings = dict(sorted(final_standings.items(), key=lambda x: x[1].get("TL_rank"), reverse=True))

    # формирование .json из словаря final_standings
    # и выгрузка final_standings.json в репо: /sub_results
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'sub_results', 'final_standings.json', \
        json.dumps(final_standings, skipkeys=True, ensure_ascii=False, indent=2))

    # формирование строки из словаря в читабельном виде
    final_standings_str = ''   # github принимает только str для записи в файл
    rank = 1
    for club in final_standings:
        final_standings_str += "{0:>2}  {1:20}   {2:3.0f}   {3:5.2f}    {4}".\
        format(str(rank), club, final_standings[club]['visual_rank'], final_standings[club]['TL_rank'], \
            final_standings[club]['nat']) + '\n'
        rank += 1

    # выгрузка standings.txt в репо: /content и /content_commits
    import os
    mod_name = os.path.basename(__file__)[:-3]
    from modules.gh_push import gh_push
    gh_push(str(mod_name), 'content', 'standings.txt', final_standings_str)
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
