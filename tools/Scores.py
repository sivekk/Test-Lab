from GitHub import *
from Labs import *
from Dir import *

class Scores:

    def __init__(this):
        #this.scoresPath = os.path.abspath(os.path.join(os.sep, 'workspaces', 'scores'))
        this.scoresPath = "scores" 
        this.scoresDir = Dir(this.scoresPath)

    def getRepos(this, repos):
        this.scoresDir.clean()
        namesRe = re.compile(".*" + repos + ".*")
        gh = GitHub()
        names = gh.getRepos(namesRe, this.scoresPath)
        return names

    def runTests(this, repoNames):
        results = {}
        lab = ".*"
        labRe = re.compile(lab)
        for name in repoNames:
            labPath = os.path.join(this.scoresPath, name)
            print("Running tests for ", labPath, "...")
            result = Labs(labPath).run(labRe, "0", verbose=True)
            results[name+":"+labPath] = result
        return results





