# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:47:33 2019

@author: bwhitehe
"""
from eLoadFuncs import *
from pSupplyFuncs import *
from mMeterFuncs import *
from fileIO import *
import visa
import sys
import time

def firstDischarge(electronics):
    eLoadSetup(electronics[0])
    v, i = getVIData(electronics[1], electronics[2])
    while(float(v) >= 2.8):
        v, i = getVIData(electronics[1], electronics[2])
    eLoadOff(electronics[0])

def charge(electronics, cycle, v, argv):
    #setup files
    print("BLAAAAAA")
    fVI, fR = makeChargeFiles(argv,"C",cycle)
    
    pSupplySetup(electronics[3])
    start_time = time.time()
    #data collection loop until charged
    while(float(v) < 3.75):
        v = dataCollection(electronics,0, start_time, fVI, fR)
    
    #clean up    
    pSupplyOff(electronics[3])
    closeFile(fVI,fR)
    
def discharge(electronics, cycle, v, argv):
    #setup files
    print("FFFFFFFFFF")
    fVI, fR = makeChargeFiles(argv,"D",cycle)
    
    eLoadSetup(electronics[0]);
    start_time = time.time()
    
    #data collection loop until discharged
    while(float(v) >= 2.8): #discharges until Volts hit low
        v = dataCollection(electronics,1, start_time, fVI, fR)
    
    #clean up
    eLoadOff(electronics[0])
    closeFile(fVI,fR)
    return 1;

def dataCollection(electronics, cOrD,start_time, fVI, fR):
    time.sleep(1.0 - ((time.time() - start_time) % 1.0))
    v, i = getVIData(electronics[1], electronics[2])
    time_now = time.time()-start_time
    if(int(round(time_now))%10 == 0):
        return v
        if(cOrD == 0):
            cResist(electronics, fR)    
        else:
            dResist(electronics, fR)
    else:
        fVI.write(("{0:d},{1:.4f},{2:.4f}\n").format(int(time_now), float(v), float(i)))
    v, i = getVIData(electronics[1], electronics[2])
    return v

def getCResist(electronics, fR, start_time):
    #inital measure
    print("REsist")
    v , i = getVIData(electronics[1], electronics[2])
    time_now = time.time() - start_time
    fR.write(("{0:d},{1:.4f}").format(int(time_now), float(i)))
    
    #turn off foor one second then measure
    pSupplyOff(electronics[3])
    time.sleep(1)
    v , i = getVIData(electronics[1], electronics[2])
    fR.write(("{0:.4f},{1:.4f}").format(float(v),float(i)))
    
    #turn on and measure within one second
    pSupplyOn(electronics[3])
    sleep(.2)
    v , i = getVIData(electronics[1], electronics[2])
    fR.write(("{0:.4f},{1:.4f}\n").format(float(v),float(i)))
    
def getDResist(electronics, fR, start_time):
    #discharging measure
    print("resisist")
    v , i = getVIData(electronics[1], electronics[2])
    time_now = time.time() - start_time
    fR.write(("{0:d},{1:.4f}").format(int(time_now), float(i)))
    #stop and measure
    eLoadOff(electronics[0])
    time.sleep(1);
    v , i = getVIData(electronics[1], electronics[2])
    fR.write(("{0:.4f},{1:.4f}").format(float(v),float(i)))
    #discharge an measure within 1 second
    eLoadOn(electronics[0])
    sleep(.2)
    v , i = getVIData(electronics[1], electronics[2])
    fR.write(("{0:.4f},{1:.4f}\n").format(float(v),float(i)))

def allOff(eLoad, pSupply):
    eLoadOff(eLoad)
    pSupplyOff(pSupply)
    time.sleep(1)
    
def eLoadSetup(eLoad):
    eLoadCCMode(eLoad)
    eLoadSetI(eLoad, 3)
    eLoadOn(eLoad)

def pSupplySetup(pSupply):
    pSupplySetV(pSupply, 4.2)
    pSupplySetI(pSupply, 1)
    pSupplyOn(pSupply)

def getVIData(mMeter1, mMeter2):
    v= mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    printVoltCurr(v,i)
    return v,i

def checkIssues(mMeter1, mMeter2):
    print("temp")
    
def printVoltCurr(v,i):
    print("Volts: {0}Current: {1}\n".format(v,i))