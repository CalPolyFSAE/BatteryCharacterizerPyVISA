#PyVisa code to test battery characterizer
#Note: this code is set up for the following devices
#eload: Kikusui PLZ303w
#pSupply: Rigol DP832
#mMeter: Rigol DM3058E


from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
from compoundFuncs import *
import visa
import time
import datetime
import os  
from os.path import join as pjoin
import sys

#Sets up connections to all devices. 
#Note the open resource input needs to be changed based to correct input,
#The correct input can found with rm.list_resources()
def setup():
    rm = visa.ResourceManager()
    print(rm.list_resources())
    
    eLoad = rm.open_resource('GPIB0::1::INSTR')
    mMeter1 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601840::INSTR')
    mMeter2 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601844::INSTR')
    pSupply = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C193604507::INSTR')
    directory = "{}_Data".format(sys.argv[1])
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)\
        
    return eLoad, mMeter1, mMeter2, pSupply

def main():
    eLoad, mMeter1, mMeter2, pSupply = setup()
    electronics = [eLoad, mMeter1, mMeter2, pSupply]
    
    #try:    
    cycle = 0
    
    while(cycle < 1):
        allOff(electronics[0],electronics[3])
        time.sleep(1)
        v = mMeterGetV(electronics[1])
        print(v)
        
        if(float(v) < 3.67):  #if charge low then charge
            charge(electronics, cycle, v, sys.argv)
        else:                #else if votls high discharge
            discharge(electronics, cycle, v, sys.argv)
    #except:
        #print("failed")
        #allOff(electronics[0],electronics[3])

if __name__ == '__main__':
   main()