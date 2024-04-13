import os, json
with open((os.path.abspath(__file__))[:-15]+'/cache/sub_results/participants.json', 'r') as j:
    tournaments = json.load(j)

participants_id = []
for ass in tournaments:
    for tourn in tournaments[ass]['tournaments']:
        for club in tournaments[ass]['tournaments'][tourn]['participants']:
            participants_id.append(club['id'])
print(participants_id)

# print(
#     [[tourn for tourn in participants[ass]['tournaments']] for ass in participants]
#     )
# print()
# print(
#     ["', '".join([tourn for tourn in participants[ass]['tournaments']]) for ass in participants]
#     )

# q = ["', '".join([tourn for tourn in participants[ass]['tournaments']]) for ass in participants]
# print(q[0])