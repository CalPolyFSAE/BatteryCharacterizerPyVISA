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
import os  
from os.path import join as pjoin


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
    
    directory = "lol"
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
    return eLoad, mMeter1, mMeter2, pSupply
def main():
    try:
        eLoad, mMeter1, mMeter2, pSupply = setup()
        cycle = 0
        
        while(cycle < 1):
            pSupplyOff(pSupply)
            eLoadOff(eLoad)
            time.sleep(1)
            v = mMeterGetV(mMeter1)
            print(v)
            if(float(v) < 3.67):  #if charge low then charge
                filepath =  "C:\\Users\\bwhitehe\\Desktop\\BatteryCharacterizerPyVISA-master\\lol\\batC{0}.csv".format(cycle+1)
                f = open(filepath, "w")
                f.write("Time,Volt,Current\n")
                pSupplySetup(pSupply)
                start_time = time.time()
                while(float(v) < 3.8): #charges until Volts hit max
                    time.sleep(1.0 - ((time.time() - start_time) % 1.0))
                    v, i = charge(mMeter1, mMeter2)
                    time_now = time.time()-start_time
                    f.write(("{0:d},{1:.4f},{2:.4f}\n").format(int(time_now), float(v), float(i)))
                    
                pSupplyOff(pSupply)
                f.close()
            else:                #else if votls high discharge
                filepath =  "C:\\Users\\bwhitehe\\Desktop\\BatteryCharacterizerPyVISA-master\\lol\\batD{0}.csv".format(cycle+1)
                f = open(filepath, "w")
                f.write("Time,Volt,Current\n")
                eLoadSetup(eLoad);
                start_time = time.time()
                while(float(v) >= 3.5): #discharges until Volts hit low
                    print("helllll")
                    time.sleep(1.0 - ((time.time() - start_time) % 1.0))
                    v,i = discharge(mMeter1, mMeter2, eLoad)
                    time_now = time.time()-start_time
                    f.write(("{0:d},{1:.4f},{2:.4f}\n").format(int(time_now), float(v), float(i)))
                eLoadOff(eLoad)
                cycle += 1
                f.close()
    except:
        print("failed")
        eLoadOff(eLoad)
        pSupplyOff(pSupply)
        

def eLoadSetup(eLoad):
    eLoadCCMode(eLoad)
    eLoadSetI(eLoad, 4)
    eLoadOn(eLoad)

def pSupplySetup(pSupply):
    pSupplySetV(pSupply, 4.2)
    pSupplySetI(pSupply, 1)
    pSupplyOn(pSupply)

def charge(mMeter1, mMeter2):
    v = mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    print("Volts: {0} Current: {1}\n".format(v,i))
    return v,i
    
def discharge(mMeter1, mMeter2, eLoad):
    v = mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    print("Volts: {0} Current: {1}\n".format(v,i))
    return v, i

def checkIssues(mMeter1, mMeter2):
    print("temp")
    

    
if __name__ == '__main__':
   main()