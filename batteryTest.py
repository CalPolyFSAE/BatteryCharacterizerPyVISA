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
    mMeter1 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601853::INSTR')
    mMeter2 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R191700643::INSTR')
    pSupply = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C192803275::INSTR')
    return eLoad, mMeter1, mMeter2, pSupply

def main():
    eLoad, mMeter1, mMeter2, pSupply = setup()
    
    pSupplyOn(pSupply)
    pSupplySetV(pSupply, 3)
    pSupplySetC(pSupply, 0.5)
    print(pSupplyGetC(pSupply))
    print(pSupplyGetV(pSupply))
    time.sleep(5)
    pSupplyOff(pSupply)




if __name__ == '__main__':
   main()