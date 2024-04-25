# модуль содержит словарь интернациональных турниров, используемых в TL
# {Association:[Short,Long,TournID,TournType]}
def int_tournaments():
    Ass_Tourn = {
                    "UEFA": 
                    [
                        ["UCL", "Champions League", 2, "League+Cup"],
                        ["UEL", "Europa League", 3, "League+Cup"],
                        ["UECL", "Conference League", 848, "League+Cup"],
                        ["USC", "UEFA Super Cup", 531, "Cup"]
                    ]
                }
    return(Ass_Tourn)                        