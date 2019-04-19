from mMeterFuncs import *
from thermocouples_reference import thermocouples

import visa
import time
import math

lengthOfTest = 1 #in min
current = 20
voltage = 12
fileName = "test1.csv" #must be .csv
pSupplyPort = 'COM3'
mMeterPort = 'USB0::0x1AB1::0x09C4::DM3R193601838::INSTR'

def setup():
    rm = visa.ResourceManager()
    print(rm.list_resources())

    pSupply = rm.open_resource(pSupplyPort)
    pSupply.baud_rate = 57600

    mMeter = rm.open_resource(mMeterPort)
    
    f = open(fileName,"w")
    f.write("Time(s),Current(A),Volt(v),Temp(f)\n")
    return f,pSupply,mMeter
    
def main():
    f,pSupply,mMeter = setup()

    pSupplySetup(pSupply)
    mMeterSetup(mMeter)
    
    startTime = time.time()
    while((time.time()-startTime) < (lengthOfTest*60)):
        time.sleep(1.0 - ((time.time() - startTime) % 1.0))
        timeNow = time.time()-startTime
        temp = getTemp(mMeter)
        print(timeNow)
        print(("{0:.4f}\n").format(float(temp)))
        f.write(("{0:d},{1:.4f},{2:.4f},{3:.4f}\n").format(int(timeNow), float(current),float(voltage), float(temp)))
        f.close()
        f = open(fileName,"a")
    
    f.close()
    pSupplyOff(pSupply)
    
    
def getTemp(mMeter):
    typeK = thermocouples['K']
    typeK
    v = mMeterGetV(mMeter)
    
    try:
        temp = typeK.emf_mVC(float(v), Tref=0) 
    except:
        print("TRUE: "+ v)
        print("UNMuliplied "+ str(float(v[11:27])))
        print("Multiplied "+ str(float(v[11:27])*(1000)))
        temp = typeK.inverse_CmV(float(v[11:27])*(1000), Tref=26) 
        print(temp)
    return temp

def pSupplySetup(pSupply):
    pSupply.write("CURR "+ str(current))
    pSupply.write("VSET "+ str(voltage))
    pSupply.write("OUT 1")
    
def mMeterSetup(mMeter):
    temp = getTemp(mMeter)
    
    
def pSupplyOff(pSupply):
    pSupply.write("OUT 0")


if __name__ == '__main__':
   main()