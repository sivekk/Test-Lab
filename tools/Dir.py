import os
import shutil

class Dir:

    def __init__(this, path):
        this.path = path

    def remove(this):
        if os.path.isdir(this.path):
            shutil.rmtree(this.path)    

    def make(this):
        if not os.path.isdir(this.path):
            os.mkdir(this.path)

    def clean(this):
        this.remove()
        this.make()

    def subdirNames(this):
        names = []
        items = os.listdir(this.path)
        for item in items:
            subdirPath = os.path.join(this.path, item)
            if os.path.isdir(subdirPath):
                names.append(item)
        return names

    def filenames(this):
        names = []
        items = os.listdir(this.path)
        for item in items:
            filePath = os.path.join(this.path, item)
            if os.path.isfile(filePath):
                names.append(item)
        return names

    def findFile(this, filenameRe):
        paths = []
        for (dirPath, dirnames, filenames) in os.walk(this.path):
            #if filename in filenames:
            for filename in filenames:
                if (filenameRe.match(filename)):
                    filePath = os.path.join(dirPath, filename)
                    paths.append(filePath)
        return paths

    
