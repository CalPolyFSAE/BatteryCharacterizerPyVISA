#Baylor Whitehead
#funcs for eload Kikusui PLZ303W

#ON/OFF
def eLoadOn(name):
    name.write("LOAD 1")
  
def eLoadOff(name):
    name.write("LOAD 0")

def eLoadState(name):
    return name.query("LOAD?")

#CCCR
def eLoadCCMode(name):
    name.write("CCCR 1")

def eLoadCRMode(name):
    name.write("CCCR 2")

def eLoadCCCRState(name):
    return name.query("CCCR?")

#CCRange
def eLoadCCRangeL(name):
    name.write('CCRANGE 0')

def eLoadCCRangeH(name):
    name.write('CCRANGE 1')

def eLoadCCRangeState(name):
    return name.query('CCRANGE?')

#CRRange
def eLoadCRRangeL(name):
    name.write('CRRANGE 0')

def eLoadCRRangeH(name):
    name.write('CRRANGE 1')

def eLoadCCRangeState(name):
    return name.query('CRRANGE?')

#CV
def eLoadCVOn(name):
    name.write("CV 1")
  
def eLoadCVOff(name):
    name.write("CV 0")

def eLoadState(name):
    return name.query("CV?")

#Current
def eLoadSetI(name, current):
    name.write("ISET {0}".format(current))

def eLoadGetI(name):
    return name.query("ISET?")

#Resistance
def eLoadSetR(name, res):
    name.write("RSET {0}".format(res))
    
def eLoadGetR(name):
    return name.query("RSET?")

#Voltage
def eLoadSetV(name, volt):
    name.write("VSET {0}".format(volt))
    
def eLoadGetV(name):
    return name.query("VSET?")

#P
def eLoadSetP(name, volt):
    name.write("PSET {0}".format(volt))
    
def eLoadGetP(name):
    return name.query("PSET?")

#input Current
def eLoadGetInI(name):
    return name.query('CURR?')

#input Volt
def eLoadGetInV(name):
    return name.query('VOLT?')    

#input Pow
def eLoadGetInP(name):
    return name.query('POW?')    