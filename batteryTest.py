#PyVisa code to test battery characterizer
#Note: this code is set up for the following devices
#eload: Kikusui PLZ303w
#pSupply: Rigol DP832
#mMeter: Rigol DM3058E

#GO TO SETTINGS FILE TO SET UP

from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
from compoundFuncs import *
import testSettings

from thermocouples_reference import thermocouples
import visa
import time
import datetime
import os  
from os.path import join as pjoin
import sys
import traceback

def setup():
    rm = visa.ResourceManager()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    print(rm.list_resources())
    
    #set up connections to electronics
    eLoad = rm.open_resource(testSettings.ELOADADDRESS)
    mMeter1 = rm.open_resource(testSettings.MMETER1ADDRESS)
    mMeter2 = rm.open_resource(testSettings.MMETER2ADDRESS)
    mMeter3 = rm.open_resource(testSettings.MMETER3ADDRESS)
    pSupply = rm.open_resource(testSettings.PSUPPLYADDRESS)
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
        chargeState = True;
        while(testSettings.cycleNum < 1):
            #All off For Saftey
            allOff(electronics[0],electronics[3])
            
            #get volt/curr and check temp
            v, i = getVIData(electronics[1], electronics[2])
            checkTemp(electronics)
            #Starts by charging, Then flips back and forth based on charge
            if(chargeState = true):  #if volts low then charge
                charge(electronics, cycle, v, sys.argv)
                chargeState = False
            else:                #else if volts high discharge
                cycle += discharge(electronics, cycle, v, sys.argv)
                chargeState = True
    except:
        #prints out traceback and turns off power supply and eload
        print("failed")
        allOff(electronics[0],electronics[3])
        print("Unexpected error:"+ traceback.format_exc())
        
    #final turn off of electronics    
    allOff(electronics[0],electronics[3])

if __name__ == '__main__':
   main()