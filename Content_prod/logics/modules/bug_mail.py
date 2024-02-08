# модуль отправляет bug_files на topligahighlights@gmail.com
def bug_mail(subj_mod, msg_bug):    # принимает параметры: subj_mod - тема письма / имя файла бага; msg_bug - сообщение / описание бага
    import datetime     # модуль для определния текущей даты
    DateNowExc = str(datetime.datetime.utcnow())[:19].replace(":", "-")    # текущая дата по UTC, отформатированная под строку для имени файла
    
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    sender = 'yadserg9@yandex.ru'
    password = bug_mail_pass
    recipient = 'topligahighlights@gmail.com'
    
    msg = MIMEText(msg_bug, 'plain', 'utf-8')
    msg['Subject'] = Header(subj_mod, 'utf-8')
    msg['From'] = sender
    msg['To'] = recipient
    
    s = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    
    try:
        s.starttls()
        s.login(sender, password)
        s.sendmail(msg['From'], recipient, msg.as_string())
    except:
        message = 'bug_mail\nписьмо не отправлено'
        # создать bug_file
        with open("../bug_files/"+DateNowExc+" bug_mail.txt", 'w', encoding='utf-8') as f:  
        # директория указывается относительно файла запуска, расположенного в /logics, а не относительно файла модуля
            f.write(message)
    finally:
        s.quit()