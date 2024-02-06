# модуль отправляет bug_files на topligahighlights@gmail.com
def bug_mail(subj_mod, msg_bug):    # принимает параметры: subj_mod - тема письма / имя файла бага; msg_bug - сообщение / описание бага
    import datetime     # модуль для определния текущей даты
    DateNowExc = str(datetime.datetime.utcnow())[:19].replace(":", "-")    # текущая дата по UTC, отформатированная под строку для имени файла

    import smtplib
    sender = 'xoserg9@gmail.com'
    password = ""
    recipient = 'topligahighlights@gmail.com'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg_bug)
    except:
        message = 'bug_mail\nписьмо не отправлено'
        # создать bug_file
        with open("../../bug_files/"+DateNowExc+" bug_mail.txt", 'w', encoding='utf-8') as f:
            f.write(message)