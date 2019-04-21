#PyVisa code to test battery characterizer
#Note: this code is set up for the following devices
#eload: Kikusui PLZ303w
#pSupply: Rigol DP832
#mMeter: Rigol DM3058E


from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
from compoundFuncs import *
from thermocouples_reference import thermocouples
import visa
import time
import datetime
import os  
from os.path import join as pjoin
import sys
import traceback

#Sets up connections to all devices. 
#Note the open resource input needs to be changed based to correct input,
#The correct input can found with rm.list_resources()
def setup():
    rm = visa.ResourceManager()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    print(rm.list_resources())
    
    #set up connections to electronics
    eLoad = rm.open_resource('GPIB0::1::INSTR')
    mMeter1 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601853::INSTR')
    mMeter2 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R191700643::INSTR')
    mMeter3 = rm.open_resource('USB0::0x1AB1::0x09C4::DM3R193601754::INSTR')
    pSupply = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C192803275::INSTR')
    directory = "{}_Data".format(sys.argv[1])
    
    #set up folder based on battery name
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)\
        
    #put the electronics into an array to pass around    
    electronics = [eLoad, mMeter1, mMeter2, pSupply, mMeter3]
    return electronics

def main():
    #sets up electronics and directory
    electronics = setup()  
    
    #Try Except For Saftey, If Failure Then turns off
    try:    
        cycle = 0

        #First discharge setup
        allOff(electronics[0],electronics[3])
        firstDischarge(electronics)
    
        #Main Loop
        while(cycle < 1):
            #All off For Saftey
            allOff(electronics[0],electronics[3])
            
            #get volt/curr and check temp
            v, i = getVIData(electronics[1], electronics[2])
            checkTemp(electronics)
            #Starts by charging, Then flips back and forth based on charge
            if(float(v) < 3.1):  #if volts low then charge
                charge(electronics, cycle, v, sys.argv)
            else:                #else if volts high discharge
                cycle += discharge(electronics, cycle, v, sys.argv)
    except:
        #prints out traceback and turns off power supply and eload
        print("failed")
        allOff(electronics[0],electronics[3])
        print("Unexpected error:"+ traceback.format_exc())
        
    #final turn off of electronics    
    allOff(electronics[0],electronics[3])

if __name__ == '__main__':
   main()