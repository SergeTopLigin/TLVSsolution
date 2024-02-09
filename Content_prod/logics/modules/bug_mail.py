# модуль отправляет bug_files на topligahighlights@gmail.com
def bug_mail(subj_mod, msg_bug):    # принимает параметры: 
# subj_mod - тема письма / имя файла бага
# msg_bug - сообщение / описание бага
    
    try:

        import os
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        sender = 'yadserg9@yandex.ru'
        password = os.getenv('bug_mail_pass')
        recipient = 'topligahighlights@gmail.com'
        
        msg = MIMEText(msg_bug, 'plain', 'utf-8')
        msg['Subject'] = Header(subj_mod, 'utf-8')
        msg['From'] = sender
        msg['To'] = recipient
    
        s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    
        s.starttls()
        s.login(sender, password)
        s.sendmail(msg['From'], recipient, msg.as_string())
        s.quit()

    except:

        # запись ошибки/исключения в переменную через временный файл
        import traceback
        with open("bug_file.txt", 'w+') as f:
            traceback.print_exc(file=f)     # создание на вирт машине файла ошибки с указанием файла кода и строки исключения
            f.seek(0)                       # установка курсора в начало временного файла
            bug_info = f.read()

        # отправка bug_file в репозиторий GitHub
        from gh_push import gh_push
        import os
        gh_push(os.path.basename(__file__)[:-3], 'bug_files', 'bug_file', 'не удалось отправить bug_mail\n'+str(bug_info))
