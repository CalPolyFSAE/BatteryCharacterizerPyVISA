#PyVisa code to test battery characterizer
#Note: this code is set up for the following devices
#eload: Kikusui PLZ303w
#pSupply: Rigol DP832
#mMeter: Rigol DM3058E


from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
import visa
import time
import datetime


#Sets up connections to all devices. 
#Note the open resource input needs to be changed based to correct input,
#The correct input can found with rm.list_resources()
def setup():
    rm = visa.ResourceManager()
    print(rm.list_resources())
    
    eLoad = rm.open_resource('GPIB0::1::INSTR')
    mMeter1 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601857::INSTR')
    mMeter2 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601841::INSTR')
    pSupply = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C192803285::INSTR')
    return eLoad, mMeter1, mMeter2, pSupply

def main():
    eLoad, mMeter1, mMeter2, pSupply = setup()
    
    cycle = 0
    while(cycle < 2):
        v = mMeterGetV(mMeter2)
        if(float(v) < 4.1):
            pSupplySetup(pSupply)
            while(float(v) < 4.1):
                v = charge(mMeter1, mMeter2)
            pSupplyOff(pSupply)
        else:            
            eLoadSetup(eLoad);
            while(float(v) >= 2.8):
                v = discharge(mMeter1, mMeter2)
            eLoadOff()
            cycle += 1
        

def eLoadSetup(eLoad):
    eLoadCCMode(eLoad)
    eLoadSetI(eLoad, 5)

def pSupplySetup(pSupply):
    pSupplySetV(pSupply, 4.2)
    pSupplySetI(pSupply, 1)
    pSupplyOn(pSupply)

def charge(mMeter1, mMeter2):
    v = mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    time.sleep(1)
    return v
    
def discharge(mMeter1, mMeter2, eLoad):
    v = mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    time.sleep(1)
    return v

if __name__ == '__main__':
   main()