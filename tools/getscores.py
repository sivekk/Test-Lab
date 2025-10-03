#!/usr/bin/env python
import time
from Scores import *

if len(sys.argv) > 1:
    repos = sys.argv[1]

scores = Scores()
repoNames = scores.getRepos(repos)

results = scores.runTests(repoNames)
students = {
    #"wolju67"           :"00auditing", 
    #"taggerungprime"    :"Rutherford, Thomas",
    #"triri66"           :"Tripathi, Ritee",
    #"LucaForc"          :"Forcatto, Luca",
    #"MushroomSoup07"    :"Burkhalter, Ainsley",
    #"Afsar"             :"Afsar, Haider",
    #"JudahJSJJ"         :"Johnson, Judah",
    #"dubs"              :"Woodard, Oliver",
    #"mccormickjime"     :"00me",
    "payma18"           :"APCS: Pays-Volard, Max",
    "rodbo27"           :"APCS: Rodionov, Boris",
    "casma17"           :"APCS: Casterella, Matthew",
    "ityfy5"            :"ITP5: Tahir, Riyan",
    "JetDoesCoding"     :"IA: Juliet",
    "Tiny-Terror-Evan"  :"ITP5: Van Pelt, Evan",
    "ozempicbeast17"    :"ITP7: Wei, Kaylee",
    "Windler11831"      :"ITP5: Windler, Abi",
    "zhary99"           :"ITP7: Zhang, Ryan",
    "abva41"            :"ITP5: Athearn, Vincent",
    "Andrew97Paul"      :"IA: Andrew",
    "dieow45"           :"ITP5: Diehl, Owen",
    "GRAE110509"        :"ITP5: Elgard, Graeden",
    "Rowan061209"       :"ITP7: Flaitz, Rowan",
    "JacobGeyser"       :"ITP7: Geyser, Jacob",
    "JtGrosz"           :"ITP5: Grosz, Jackson",
    "JaronHeine"        :"ITP7: Heine, Jaron",
    "ERROR4682"         :"ITP5: Hermon, Leo",
    "GabrielHundley"    :"ITP7: Hundley, Gabriel",
    "HutchRox"          :"ITP7: Hutchins, David",
    "joban48"           :"ITP7: Jobman, Andrew",
    "Calebk2008"        :"ITP7: Kearney, Caleb",
    "yomamma38050"      :"ITP5: Kozar, Mark",
    "lacjo08"           :"ITP7: Lacy, Josiah",
    "Scrubbey-Dubbey-Patrick"     :"ITP5: McCarron, Patrick",
    "Xerquees"          :"ITP7: Montez, Amelia",
    "NickMason42"       :"ITP7: Panella, Nicholas",
    "rehle49"           :"ITP7: Rehme, Levi",
    "rosma-28"          :"ITP7: Ross, Matthew",
    #"com"               :"00me"
}
studentResults = {} 
for dir in results:
    #login = dir.split("-").pop()
    labNameList = dir.split("lab_").pop().split("-")
    labNameList.pop(0)
    login = "-".join(labNameList)
    if not login in students:
        continue
    student = students[login]
    studentResults[student] = results[dir]
for student in sorted(studentResults.keys()):
    results = studentResults[student]
    print(student, ":", studentResults[student])
        