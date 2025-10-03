
class BuildType:

  def __init__(this, type):
    this.type = type 

  def getType(this):
    return this.type
    
  def filterStart(this, line):
    if this.type == "SOLUTION":
      if ((line.strip() == "# TEMPLATE ONLY - START:") or
          (line.strip() == "// TEMPLATE ONLY - START:")  ):
        return True
    else:
      if ((line.strip() == "# SOLUTION ONLY - START:") or
          (line.strip() == "// SOLUTION ONLY - START:")  ):
        return True
    return False

  def filterStop(this, line):
    if this.type == "SOLUTION":
      if ((line.strip() == "# TEMPLATE ONLY - END:") or
          (line.strip() == "// TEMPLATE ONLY - END:")  ):
        return True
    else:
      if ((line.strip() == "# SOLUTION ONLY - END:") or
          (line.strip() == "// SOLUTION ONLY - END:")  ):
        return True
    return False

# end class BuildType