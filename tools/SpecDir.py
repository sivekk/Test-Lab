import os
import shutil
import re
import filecmp

class SpecDir:
  
  def __init__(this, path, template):
    this.path               = path
    this.dirName            = os.path.basename(this.path)
    if (template == "new"):
      this.template = None
      this.makeNewDir()
    else:
      this.template = template
    #this.copyTemplate()
    this.files              = {}
    this.pyHeaderFileName   = "header.py"
    this.javaHeaderFileName = "header.java"
    this.pyFooterFileName   = "footer.py"
    this.javaFooterFileName = "footer.java"
    this.pyFileName         = this.readPyFileName()
    this.readFileFragments()

  def makeNewDir(this):
    if os.path.exists(this.path):
      shutil.rmtree(this.path)
    os.mkdir(this.path)

  def getPath(this):
    return this.path

  def readPyFileName(this):
    for name in os.listdir(this.path):
      if name.split(".")[-1] == "py":
        return name

  @staticmethod
  def printFiles(files):
    for filename in files:
      print("file:", filename)
      for line in files[filename]:
        print(line)
      print()
      
  def getFiles(this):
    return this.files
    
  def addHeaderToFileFragments(this, fragments):
    print("addHeader")
    pyHeader   = this.pyHeaderFileName in os.listdir(this.path) 
    pyFooter   = this.pyFooterFileName in os.listdir(this.path) 
    javaHeader = this.javaHeaderFileName in os.listdir(this.path) 
    javaFooter = this.javaFooterFileName in os.listdir(this.path) 

    pyHeaderLines = []
    if pyHeader: 
      pyHeaderFilePath = os.path.join(this.path, this.pyHeaderFileName)
      print("add pyHeader path:", pyHeaderFilePath)
      pyHeaderFile = open(pyHeaderFilePath)
      pyHeaderLines = pyHeaderFile.readlines()
      pyHeaderFile.close()
    
    pyFooterLines = []
    if pyFooter: 
      pyFooterFilePath = os.path.join(this.path, this.pyFooterFileName)
      pyFooterFile = open(pyFooterFilePath)
      pyFooterLines = pyFooterFile.readlines()
      pyFooterFile.close()
    
    javaHeaderLines = []
    if javaHeader:
      javaHeaderFilePath = os.path.join(this.path, this.javaHeaderFileName)
      javaHeaderFile = open(javaHeaderFilePath)
      javaHeaderLines = javaHeaderFile.readlines()
      javaHeaderFile.close()

    javaFooterLines = []
    if javaFooter:
      javaFooterFilePath = os.path.join(this.path, this.javaFooterFileName)
      javaFooterFile = open(javaFooterFilePath)
      javaFooterLines = javaFooterFile.readlines()
      javaFooterFile.close()

      for name in fragments:
        if (name.split(".").pop() == "py"):
          print("Adding header to:", name)
          fragments[name] = pyHeaderLines + fragments[name] + pyFooterLines 
        elif (name.split(".").pop() == "java"):
          fragments[name] = javaHeaderLines + fragments[name] + javaFooterLines 

    return fragments

  def mergeFileFragments(this, fragments):
    for filename in fragments:
      newFileName = this.strFromTemplateStr(filename)
      if (this.files.get(newFileName) == None):
        this.files[newFileName] = fragments[filename]
      else:
        this.files[newFileName] = this.files[newFileName] + fragments[filename]
      this.files[newFileName] = this.fileFromTemplateFile(this.files[newFileName])
      
  def getFileFragments(this):
    this.readFileFragments()
    return this.files

  def getSubDirFileFragments(this, subDirName):
    subDirPath = os.path.join(this.path, subDirName)
    if os.path.isdir(subDirPath):
      subDir = SpecDir(subDirPath, None)
      #fragments = subDir.getFileFragments()
      fragments = subDir.getFiles()
    else:
      fragments = {}
    return fragments

  def makeMDCodeSection(this, lines):
    newLines = []
    for line in lines:
      newLines.append("\t" + line)
    return newLines 

  def strFromFragmentStr(this, str):
    match = re.search("<<file:([^>]+)>>", str)
    if (match != None):
      relativePath = match.group(1)
      path = os.path.join(this.path, relativePath)
      if (not os.path.exists(path)):
        print("ERROR:  File not found for:", str)
        return str
      file = open(path)
      lines = file.readlines()
      file.close()
      filestr = "".join(this.makeMDCodeSection(lines))
      str = re.sub("<<file:[^>]+>>", filestr, str) 
    return str
      
  def readFileFragments(this):
    for filename in this.fileFragmentNames():
      newFileName = this.strFromTemplateStr(filename)
      this.files[newFileName] = this.fileFromFragmentFile( this.fileFromTemplateFile(this.readFile(filename)))


  def renameInFile(this):
    (rest, tName) = os.path.split(this.path)
    (rest, testsdir) = os.path.split(rest)
    (rest, pName) = os.path.split(rest)
    newfilename = pName+"_"+tName+"_in.txt"
    oldFilePath = os.path.join(this.path, "in")
    newFilePath = os.path.join(this.path, newfilename)
    os.rename(oldFilePath, newFilePath)
    return(newfilename)

  def fileFragmentNames(this):
    ffNames = []
    for filename in this.fileNames():

      # UPGRADE old lab specifications
      if (filename == "in"):
        filename = this.renameInFile()

      fileExtension = filename.split(".").pop()
      if (((fileExtension == "py")   or 
          (fileExtension == "java") or 
          (fileExtension == "txt")  or 
          (fileExtension == "dat")  or 
          (fileExtension == "csv")  or 
          (fileExtension == "md")     )         and
          (filename != this.pyHeaderFileName)   and 
          (filename != this.javaHeaderFileName) and 
          (filename != this.pyFooterFileName)   and 
          (filename != this.javaFooterFileName)    ):
        ffNames.append(filename)
      """
      if ((filename != this.pyHeaderFileName)   and 
          (filename != this.javaHeaderFileName) and 
          (filename != this.pyFooterFileName)   and 
          (filename != this.javaFooterFileName)    ):
        ffNames.append(filename)
      """
    return ffNames
      
  def dirNames(this):
    dirNames = []
    for name in os.listdir(this.path):
      if (os.path.isdir(os.path.join(this.path, name))):
        dirNames.append(name)
    dirNames.sort()
    return dirNames

  def readFile(this, filename):
    #print("filename:", filename)
    fileObj = open(os.path.join(this.path, filename))
    return fileObj.readlines()

  def writeFile(this, filename, file, forceWrite = False):

    backupDir = os.path.join(this.path, ".backup")
    filePath  = os.path.join(this.path, filename)
    backupFilePath = os.path.join(backupDir, filename)
    
    # make .backup dir if it doesn't exist
    if not os.path.isdir(backupDir):
      os.mkdir(backupDir)

    # make backup file if it doesn't exist
    if not os.path.isfile(backupFilePath):
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

    # if file doesn't exit, make file and backup file 
    if not os.path.isfile(filePath):
      fileObj = open(filePath, "w")
      fileObj.writelines(file)
      fileObj.close() 
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

    # compare file and backup file
    fileObj = open(filePath)
    fileLines = fileObj.readlines()
    fileObj.close()
    backupFileObj = open(backupFilePath) 
    backupFileLines = backupFileObj.readlines()
    backupFileObj.close()
    filesMatch = filecmp.cmp(filePath, backupFilePath, shallow=False)

    # if no difference, write new file and new backup file
    if (filesMatch or forceWrite):
      fileObj = open(filePath, "w")
      fileObj.writelines(file)
      fileObj.close() 
    if (filesMatch and not forceWrite):
      backupFileObj = open(backupFilePath, "w")
      backupFileObj.writelines(file)
      backupFileObj.close()

  def writeFiles(this, dictionary, forceWrite = False):
    for filename in dictionary:
      this.writeFile(filename, dictionary[filename], forceWrite)
  
  def fileNames(this):
    fileNames = []
    for name in os.listdir(this.path):
      if (os.path.isfile(os.path.join(this.path, name))):
        fileNames.append(name)
    fileNames.sort()
    return fileNames 

  def fileFromFragmentFile(this, fragmentFile):
    file = []
    for line in fragmentFile:
      str = this.strFromFragmentStr(line) 
      file.append(str)
    return file
    
  def fileFromTemplateFile(this, templateFile):
    file = []
    for line in templateFile:
      str = this.strFromTemplateStr(line) 
      file.append(str)
    return file
  
  def strFromTemplateStr(this, name): 
    return name 

  def isPyFileName(this, filename):
    result = True
    parts = filename.split(".") 
    if len(parts) < 2:
      result = False 
    elif parts[1] != "py":
      result =  False 

    return result
    
  def copyTemplate(this):

    if (this.template == None):
      return
      
    # make directories
    for dirName in this.template.dirNames():
      dirName = this.strFromTemplateStr(dirName)
      if not (dirName in this.dirNames()): 
        os.mkdir(os.path.join(this.path, dirName))

    # copy files
    for templateFileName in this.template.fileNames():
      newFileName = this.strFromTemplateStr(templateFileName)
      pyFileName = this.readPyFileName()
      if (not this.isPyFileName(newFileName) or
          (pyFileName == None)               or
          (pyFileName == newFileName)          ):
        templateFile = this.template.readFile(templateFileName)
        newFile = this.fileFromTemplateFile(templateFile)
        this.writeFile(newFileName, newFile)

  @staticmethod
  def filterFile(file, buildType):
      newFile = []
      filtering = False
      for line in file:
        if buildType.filterStart(line):
          filtering = True
        if filtering == False:
          newFile.append(line)  
        if buildType.filterStop(line):
          filtering = False
      return newFile

  @staticmethod
  def filterFiles(files, buildType):
    newFiles = {}
    for filename in files:
      if filename == "header.py":
        continue;
      newFile = SpecDir.filterFile(files[filename], buildType)
      newFiles[filename] = newFile
    return newFiles
        
# end class Directory
