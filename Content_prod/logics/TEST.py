from modules.int_tournaments import int_tournaments
int_tournaments = int_tournaments()
for ass in int_tournaments:
    for tourn in int_tournaments[ass]:
        print(tourn[0], tourn[2])
