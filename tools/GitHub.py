import subprocess
import re
import sys
import os

class GitHub:

    def __init__(this):
        this.ghEnv = os.environ.copy()
        if "GITHUB_TOKEN" in this.ghEnv:
            this.ghEnv.pop("GITHUB_TOKEN")
        this.scoresAuth()

    def scoresAuth(this):
        # make sure we have needed authorization token
        goodAuth = re.compile("(?s:.)*hosts\.yml")      # ?s:.   matches newline or .
        #ghAuthCmd = ["gh", "auth", "status"]
        ghAuthCmd = ["gh auth status"]
        result = subprocess.run(ghAuthCmd, text=True, shell=True, env=this.ghEnv, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        if not (goodAuth.match(result.stdout)):
            print(result.stdout)
            sys.exit("Missing authorization.  To fix, regenerate token (https://github.com/settings/tokens/1694985723), unset GITHUB_TOKEN, and then run:  gh auth login")

    def getRepoNames(this, re):
        repoNames = []
        result = subprocess.run("gh repo list --limit 5000 liberty-common-high-school", text=True, shell=True, env=this.ghEnv, capture_output=True)
        for line in result.stdout.splitlines():
            repoName = line.split()[0]
            print("repoName:", repoName)
            if re.match(repoName):
                repoNames.append(repoName)
        return repoNames
    
    def cloneRepos(this, repoNames, targetPath):
        cloneNames = []
        for repoName in repoNames:
            subprocess.run("cd " + targetPath + " ; gh repo clone " + repoName, text=True, shell=True, env=this.ghEnv)
            cloneName = repoName.split("/")[1]
            cloneNames.append(cloneName)
        return cloneNames

    def getRepos(this, namesRe, targetPath):
        repoNames = this.getRepoNames(namesRe)
        cloneNames = this.cloneRepos(repoNames, targetPath) 
        return cloneNames