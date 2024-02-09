# тест bug_mail

try:
    q=1/0
except:
    # запись ошибки/исключения в переменную через временный файл
    import traceback
    with open("bug_file.txt", 'w+') as f:
        traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
        f.seek(0)                       # установка курсора в начало временного файла
        bug_info = f.read()

    # отправка bug_file на почту
    from modules.bug_mail import bug_mail
    import os
    bug_mail(os.path.basename(__file__)[:-3], str(bug_info))
