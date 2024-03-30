# определение участников от нац кубка
# возвращает список участников = [{club: , id: }, ...]

# текущая стадия (1/8, 1/4 итд): последняя несыгранная, если известны все ее участники, или финал
# если количество участников текущей стадии равно квоте: все участники текущей стадии
# если количество участников текущей стадии больше квоты: победитель турнира или лучшие среди участников текущей стадии
# если количество участников текущей стадии меньше квоты: все участники текущей стадии + лучшие среди участников предыдущей стадии
# критерии определения лучших участников стадии:
    # 1. TL_rank (own curr + passed rivals on round date) +1.2 >=0
    # 2. PTS/PL
    # 3. DIF/PL
    # 4. TL standings
    # 5. random

# определение участников происходит по fixtures
# актуализация fixtures в cup_files, вызываемого из tournaments

def participants_nat_cup(tourn, tourn_id, season, quota, prev):
    # tourn = tournaments.json[nat]['tournaments'][tourn]['tytle']
    # tourn_id = tournaments.json[nat]['tournaments'][tourn]['id']
    # season = tournaments.json[nat]['tournaments'][tourn]['season']   YY-YY
    # quota = tournaments.json[nat]['tournaments'][tourn]['quota']
    # prev = список участников от cup PREV season = [{club: , id: }, ...]

    try:    # обработка исключений для определения ошибки и записи ее в bug_file в блоке except

        participants = []   # результирующий список участников от турнира
        import os
        import json
        import random
        with open((os.path.abspath(__file__))[:-39]+'/cache/sub_results/final_standings.json', 'r') as j:
            TL_standings = json.load(j)

        file_find = 0   # флаг наличия файла турнира
        for tourn_file in os.listdir((os.path.abspath(__file__))[:-39]+'/cache/answers/fixtures'):
            if tourn in tourn_file and season in tourn_file:
                file_find = 1
                with open((os.path.abspath(__file__))[:-39]+'/cache/answers/fixtures/'+tourn_file, 'r') as j:
                    tourn_fixtures = json.load(j)
                break
        
        if file_find == 1:



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
        
        return([])
