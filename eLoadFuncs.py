#Baylor Whitehead
#funcs for eload Kikusui PLZ303W

def eLoadSetV(name, volt):
    name.write("VSET {0}".format(volt))
    
def eLoadGetV(name):
    return name.query("VSET?")
    
def eLoadOn(name):
    name.write("LOAD 1")
  
def eLoadOff(name):
    name.write("LOAD 0")

def eLoadSetI(name, current):
    name.write("ISET {0}".format(current))
    
def eLoadGetI(name):
    return name.query("ISET?")