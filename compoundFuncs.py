#PyVisa code to test battery characterizer
#Note: this code is set up for the following devices
#eload: Kikusui PLZ303w
#pSupply: Rigol DP832
#mMeter: Rigol DM3058E

from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
from fileIO import *
import testSettings

from thermocouples_reference import thermocouples
import visa
import sys
import time

def firstDischarge(electronics):
    print("-------------------FIRST DISCHARGE-----------------")
    #set up eLoad and get first v value
    eLoadSetup(electronics[0])
    v, i = getVIData(electronics[1], electronics[2])
    
    #checks voltage during discharge until under 2.8 volts
    count = 0
    start_time = time.time()
    while(float(v) >= 2.8):
        #incriment counter, wait till end of second, get data
        count += 1
        time.sleep(1.0 - ((time.time() - start_time) % 1.0))
        v, i = getVIData(electronics[1], electronics[2])
        
        #when counter is 10 aka 10 seconds have passes check temp
        if((count) %10  == 0):
            checkTemp(electronics)
            if(count % 1000000 == 0): # prevents overflow
                count = 0
                
    #turns off eload    
    eLoadOff(electronics[0])


def finalCharge(electronics):
    print("----------------CHARGE-------------------")
    #setting up psupply to charge to about 80% for storage
    pSupplySetup(electronics[3])
    v, i = getVIData(electronics[1], electronics[2])
    
    #data collection loop until charged
    count = 0
    start_time = time.time()
    while(float(v) < testSettings.FINALVOLT):
        #incriment counter, wait till end of second
        count += 1
        time.sleep(1.0 - ((time.time() - start_time) % 1.0))
        v, i = getVIData(electronics[1], electronics[2])
        
        #when counter is 10 aka 10 seconds have passes check temp
        if((count) %10  == 0):
            checkTemp(electronics)
            if(count % 1000000 == 0): #prevents overflow
                count = 0
    
    #pSupply off and closes files
    pSupplyOff(electronics[3])
    
    
def charge(electronics, cycle, v, argv):
    print("----------------CHARGE-------------------")
    #setting up files and psupply
    fVI, fR = makeChargeFiles(argv,"C",cycle)
    pSupplySetup(electronics[3])
    
    count = 0
    #data collection loop until charged
    start_time = time.time()
    while(float(v) < testSettings.UPPERVOLTLIMIT):
        #incriment counter and Data Collection
        count += 1
        v = dataCollection(electronics,0, start_time, fVI, fR, count)
        #every 10ish seconds opens and closes file to update it, and checks temp
        if((count) %10  == 0):
            fVI,fR = openCloseFile(fVI, fR, argv,"C",cycle)
            checkTemp(electronics)
            if(count % 1000000 == 0): #prevents overflow
                count = 0
    
    #pSupply off and closes files
    pSupplyOff(electronics[3])
    closeFile(fVI,fR)
    
def discharge(electronics, cycle, v, argv):
    print("-----------------DISCHARGE-----------------")
    #setup files and set up eload
    fVI, fR = makeChargeFiles(argv,"D",cycle)
    eLoadSetup(electronics[0]);
    
    count = 0
    #data collection loop until discharged
    start_time = time.time()
    while(float(v) >= testSettings.LOWERVOLTLIMIT): #discharges until Volts hit low
        #incimrents counter and Data Collection
        count +=1
        v = dataCollection(electronics,1, start_time, fVI, fR,count)
        #every 10ish seconds opens and closes file to update it, and checks temp
        if((count) %10 == 0):
            fVI,fR = openCloseFile(fVI,fR, argv, "D", cycle)
            checkTemp(electronics)
            if(count % 1000000 == 0): #prevents overflow
                count = 0
    
    #turns of eload and closes files and retruns 1 to incriment cycle counter
    eLoadOff(electronics[0])
    closeFile(fVI,fR)
    return 1;

def dataCollection(electronics, cOrD,start_time, fVI, fR,count):
    #sleeps till end of next second marker so that data is collected at second marks
    time.sleep(1.0 - ((time.time() - start_time) % 1.0))
    #gets data
    v, i = getVIData(electronics[1], electronics[2])
    time_now = time.time()-start_time #gets current time
    if(count %30 == 0): #every 30 data collections it will do a resistance calculation
        if(cOrD == 0):
            getCResist(electronics, fR, start_time)    
        else:
            getDResist(electronics, fR, start_time)
        return v
    #writes data to VI file
    fVI.write(("{0:d},{1:.4f},{2:.4f}\n").format(int(time_now), float(v), float(i)))
    return v

def getCResist(electronics, fR, start_time):
    #inital measure
    print("-------------RESIST-------------------")
    v1 , i1 = getVIData(electronics[1], electronics[2])
    time_now = time.time() - start_time
 
    #turn off foor one second then measure
    pSupplyOff(electronics[3])
    time.sleep(1)
    v2 , i2 = getVIData(electronics[1], electronics[2])
    
    #turn on and measure within one second
    pSupplyOn(electronics[3])
    time.sleep(1)
    v3 , i3 = getVIData(electronics[1], electronics[2])
    #writes all 7 values to file
    fR.write(("{0:d},{1:.4f},{2:.4f},{3:.4f},{4:.4f},{5:.4f},{6:.4f}\n").format(int(time_now),
              float(v1),float(i1),float(v2),float(i2),float(v3),float(i3)))
    
def getDResist(electronics, fR, start_time):
    #discharging measure
    print("-------------RESIST-------------------")
    v1 , i1 = getVIData(electronics[1], electronics[2])
    time_now = time.time() - start_time
    #stop and measure
    eLoadOff(electronics[0])
    time.sleep(1);
    v2 , i2 = getVIData(electronics[1], electronics[2])
    #discharge an measure within 1 second
    eLoadOn(electronics[0])
    time.sleep(1)
    v3 , i3 = getVIData(electronics[1], electronics[2])
    #writes all 7 values to file
    fR.write(("{0:d},{1:.4f},{2:.4f},{3:.4f},{4:.4f},{5:.4f},{6:.4f}\n").format(int(time_now),
              float(v1),float(i1),float(v2),float(i2),float(v3),float(i3)))

def allOff(eLoad, pSupply): # turns off eload and psupply
    eLoadOff(eLoad)
    pSupplyOff(pSupply)
    time.sleep(1)
    
def eLoadSetup(eLoad): # sets up eload
    eLoadCCMode(eLoad)
    eLoadSetI(eLoad, testSettings.ELOADCURR)
    eLoadOn(eLoad)

def pSupplySetup(pSupply): #sets up psupply
    pSupplySetV(pSupply, testSettings.PSUPPLYVOLT)
    pSupplySetI(pSupply, testSettings.PSUPPLYCURR)
    pSupplyOn(pSupply)

def getVIData(mMeter1, mMeter2): #gets V/I data and prints/returns it
    v= mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    printVoltCurr(v,i)
    return v,i
    
def printVoltCurr(v,i): # prints Volt/Curr
    print("-------------Voltage and Current-------------------")
    print("Volts: {0}Current: {1}\n".format(v,i))
    
    
def checkTemp(electronics): # checks temp and if over limit then turns off psupply/eload and ends program
    #setting up thermocouple
    typeK = thermocouples['K']
    typeK
    #getting voltage
    v = mMeterGetV(electronics[4])
    #calcualtes temp
    try:
        temp = typeK.emf_mVC(float(v), Tref=0) 
        print("TEMP: " + temp)
    except:
        print("--------------TEMP CHECK---------------------")
        print("TRUE: "+ str(v))
        print("Multiplied "+ str(float(v)*(1000)))
        temp = typeK.inverse_CmV(float(v)*(1000), Tref=23) 
        print("TEMP: " + str(temp) + "\n")
    #checks if temp is to high
    if(temp > testSettings.MAXTEMP):
        allOff(electronics[0],electronics[3])
        print("O Shit this is fire")
        print("we burnin")
        sys.exit()
    
    
    return temp
    