#Baylor Whitehead
#funcs for pSupply RIGOL DP832

#ON/OFF
def pSupplyOn(name):
    name.write('OUTPut CH1, ON')

def pSupplyOff(name):
    name.write('OUTPut CH1, OFF')
    
def pSupplyState(name):
    name.write('OUTPut? CH1')
    
#Voltage    
def pSupplySetV(name, volt):   
    name.write('SOURce1:VOLTage {0}'.format(volt))

def pSupplyGetV(name):
    return name.query("VOLT?")

#Current
def pSupplySetI(name, current):   
    name.write('SOURce1:CURRent {0}'.format(current))

def pSupplyGetI(name):
    return name.query("CURR?")