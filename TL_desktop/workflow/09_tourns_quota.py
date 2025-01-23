# корректировка квоты в 10_participants.json

import os, json
with open((os.path.abspath(__file__))[:-28]+'/cache/tournaments.json', 'r', encoding='utf-8') as j:
    tournaments = json.load(j)
with open((os.path.abspath(__file__))[:-28]+'/workflow/10_participants.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)

# удаление ассоциаций с квотой 0
ass_del = []
for ass in participants:
    if ass not in tournaments:
        ass_del.append(ass)
for ass in ass_del:
    participants.pop(ass)

for ass in tournaments:
    if ass in participants:
        for tourn in tournaments[ass]['tournaments']:
            if tourn in participants[ass]['tournaments']:
                participants[ass]['tournaments'][tourn]['rating'] = tournaments[ass]['tournaments'][tourn]['rating']
                participants[ass]['tournaments'][tourn]['quota'] = tournaments[ass]['tournaments'][tourn]['quota']
            else:   # если появился новый турнир
                participants[ass]['tournaments'][tourn] = tournaments[ass]['tournaments'][tourn]
    else:   # если появилась новая ассоциация с квотой > 0
        participants[ass] = tournaments[ass]

# print(json.dumps(participants, skipkeys=True, ensure_ascii=False, indent=2))

# формирование .json из словаря participants
with open((os.path.abspath(__file__))[:-28]+'/workflow/10_participants.json', 'w', encoding='utf-8') as j:
    json.dump(participants, j, skipkeys=True, ensure_ascii=False, indent=2)
