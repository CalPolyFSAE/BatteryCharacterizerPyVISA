from mMeterFuncs import *


import visa
import time
import math

lengthOfTest = 1 #in min
current = 1
voltage = 1
fileName = "test1.csv" #must be .csv
pSupplyPort = 'ASRL3::INSTR'
mMeterPort1 = 'USB0::0x1AB1::0x09C4::DM3R193601828::INSTR'
mMeterPort2 = 'USB0::0x1AB1::0x09C4::DM3R193601838::INSTR'

def setup():
    rm = visa.ResourceManager()
    print(rm.list_resources())

    pSupply = rm.open_resource(pSupplyPort)
    pSupply.baud_rate = 57600

    mMeter1 = rm.open_resource(mMeterPort1)
    mMeter2 = rm.open_resource(mMeterPort2)
    
    f = open(fileName,"w")
    f.write("Time(s),Rest1(Ohms),Temp1(C),Rest2(Ohms),Temp2(C)\n")
    return f,pSupply,mMeter1,mMeter2
    
def main():
    f,pSupply,mMeter1,mMeter2 = setup()

    pSupplySetup(pSupply)
    mMeterSetup(mMeter1,mMeter2)
    
    startTime = time.time()
    while((time.time()-startTime) < (lengthOfTest*60)):
        time.sleep(1.0 - ((time.time() - startTime) % 1.0))
        timeNow = time.time()-startTime
        c1, c2, r1, r2 = getTemp(mMeter1,mMeter2)
        print(timeNow)
        print(("R1: {0:.4f} C1: {1:.4f} R2: {2:.4f} C2: {3:.4f} \n").format(r1, c1, r2, c2))
        f.write(("{0:d},{1:.4f},{2:.4f},{3:.4f},{4:.4f}\n").format(
                int(timeNow), float(r1),float(c1), float(r2), float(c2)))
        f.close()
        f = open(fileName,"a")
    
    f.close()
    pSupplyOff(pSupply)
    
    
def getTemp(mMeter1,mMeter2):
    B = 3575
    R0 = 10000
    T0 = 298
    Rinf = R0*math.exp((-1*B)/T0)
    
    try:
        r1 = float(mMeterGetR(mMeter1))
        
        c1 = B/math.log(r1/Rinf,math.e) - 273
    except:
        r1 = mMeterGetR(mMeter1)
        r1 = float(r1[11:27])
        c1 = B/math.log(r1/Rinf,math.e) - 273
    try:
        
        r2 = float(mMeterGetR(mMeter2))
        
        c2 = B/math.log(r2/Rinf,math.e) - 273
    except:
        
        
        r2 = mMeterGetR(mMeter2)
    
        r2 = float(r2[11:27])
        
        c2 = B/math.log(r2/Rinf,math.e) - 273
        
    
    return c1,c2,r1,r2

def pSupplySetup(pSupply):
    pSupply.write("CURR "+ str(current))
    pSupply.write("VSET "+ str(voltage))
    pSupply.write("OUT 1")
    
def mMeterSetup(mMeter1,mMeter2):
    mMeterGetR(mMeter1)
    mMeterGetR(mMeter2)

    
def pSupplyOff(pSupply):
    pSupply.write("OUT 0")


if __name__ == '__main__':
   main()