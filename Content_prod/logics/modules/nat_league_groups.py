# модуль определения стадий нац лиг (в standings ключ group)
# если в запросе standings: в списке standings_dict['response'][0]['league']['standings'] более одного элемента:
    # добавить ассоциацию в sub_results в nat_league_groups.json и 
    # отправить на mail уведомление о необходимости сортировки groups
# формировать club_set в tournaments.py и набирать participants из groups в порядке их сортировки
# в начале нового сезона чистить nat_league_groups.json