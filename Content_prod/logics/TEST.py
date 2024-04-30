import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants_nat.json', 'r', encoding='utf-8') as j:
    participants = json.load(j)
participants_id = []    # список id участников
for ass in participants:
    for club in participants[ass]:
        participants_id.append(club['id'])
print(participants_id)