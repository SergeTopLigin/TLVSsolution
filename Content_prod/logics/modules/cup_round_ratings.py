# определение рейтингов раундов кубка:
# текущего - по текущим standings
# предыдущих - по standings, актуальных на момент окончания последнего матча стадии (/standings_history)


def cup_round_ratings(cup, season, fixtures_dict):
    # cup - в соответствии ass[0] nat_tournaments.py
    # season = YY-YY
    # fixtures_dict - словарь ответа на запрос fixtures кубка
    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except
        # формирование списка словарей: cup_round_ratings_list = [{round: 'name', last_date: timestamp, clubID_set: [ID, ...], rating: float}, ...]
        # фиксирование раундов из fixtures_dict в cup_round_ratings_list

        # проверка наличия файла кубка в /cup_round_ratings

        # проверка наличия рейтингов предыдущих раундов в файле

        # расчет рейтингов отсутствующих предыдущих раундов

        # расчет рейтинга текущего раунда (TL_standings каждый день изменяется)


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