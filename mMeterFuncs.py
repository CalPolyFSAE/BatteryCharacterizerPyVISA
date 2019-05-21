#Baylor Whitehead
#funcs for mMeter RIGOL DM3058E

#volt
def mMeterGetV(name):
    return name.query(":MEASure:VOLTage:DC?")

#current
def mMeterGetI(name):
    return name.query(":MEASure:CURRent:DC?")

#current
def mMeterGetR(name):
    return name.query(":MEASure:RESistance?")