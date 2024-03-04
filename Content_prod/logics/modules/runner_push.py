# отправка файла на текущий runner
def runner_push(main_mod, file_dir, file_name, file_content):
# main_mod = имя файла запуска задачи
# file_dir = каталог размещения файла в репо
# file_name = имя файла с расширением (пр: example.txt)
# file_content = содержание файла
# в file_dir досаточно указать папку, в которую надо сохранить файл: функция определит весь путь
# при отправке в bug_files указать file_name = bug_file: функция составит имя из даты и main_mod
    
    try:

        # определение каталога сохранения файла (на runner требуются не все каталоги)
        # if file_dir == 'bug_files':             path = 'Content_prod/bug_files/'
        if file_dir == 'answers':               path = 'Content_prod/cache/answers/'
        if file_dir == 'standings':             path = 'Content_prod/cache/answers/standings/'
        if file_dir == 'fixtures':              path = 'Content_prod/cache/answers/fixtures/'
        if file_dir == 'sub_results':           path = 'Content_prod/cache/sub_results/'
        if file_dir == 'club_sets':             path = 'Content_prod/cache/sub_results/club_sets/'
        if file_dir == 'cup_round_ratings':     path = 'Content_prod/cache/sub_results/cup_round_ratings/'
        # if file_dir == 'content_commits':       path = 'Content_prod/cache/content_commits/'
        if file_dir == 'content':               path = 'TL_VS_project/TL_flask/static/content/'

        # создание файла
        import os
        with open((os.path.abspath(__file__))[:-42]+path+file_name, 'w', encoding='utf-8') as f:
            if file_name[-3:] == 'txt':
                f.write(file_content)
            elif file_name[-4:] == 'json':
                import json
                json.dump(file_content, f, skipkeys=True, ensure_ascii=False, indent=2)
    
    except:

        # запись ошибки/исключения в переменную через временный файл
        import traceback
        with open("bug_file.txt", 'w+') as f:
            traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
            f.seek(0)                       # установка курсора в начало временного файла
            bug_info = f.read()

        # отправка bug_file на почту и в репо
        import os
        mod_name = os.path.basename(__file__)[:-3]
        from modules.bug_mail import bug_mail
        bug_mail(str(mod_name), 'не удалось отправить файл на runner\n'+str(bug_info))
        from modules.gh_push import gh_push
        gh_push(str(mod_name), 'bug_files', 'bug_file', 'не удалось отправить файл на runner\n'+str(main_mod)+'\n'+str(bug_info))
