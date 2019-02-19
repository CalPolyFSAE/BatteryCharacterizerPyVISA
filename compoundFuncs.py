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

def charge(electronics, cycle, v, argv):
    fVI, fR = makeChargeFiles(argv,cycle)
    pSupplySetup(electronics[3])
    start_time = time.time()
    
    while(float(v) < 3.8): #charges until Volts hit max
        v = dataCollection(electronics,0, start_time, fVI, fR)
        
    pSupplyOff(electronics[3])
    closeFiles(fVI,fR)
    
def discharge(electronics, cycle, v, argv):
    fVI, fR = makeChargeFiles(argv,cycle)
    eLoadSetup(electronics[0]);
    start_time = time.time()
    
    while(float(v) >= 3.5): #discharges until Volts hit low
        v = dataCollection(electronics,1, start_time, fVI, fR)
    
    eLoadOff(electronics[0])
    cycle += 1
    closeFiles(fVI,fR)

def dataCollection(electronics, cOrD,start_time, fVI, fR):
    time.sleep(1.0 - ((time.time() - start_time) % 1.0))
    v, i = getVIData(electronics[1], electronics[2])
    time_now = time.time()-start_time
    if(int(round(time_now))%10 == 0):
        if(cOrD == 0):
            cResist(electronics, fR)    
        else:
            dResist(electronics, fR)
    else:
        fVI.write(("{0:d},{1:.4f},{2:.4f}\n").format(int(time_now), float(v), float(i)))
    
    return v

def cResist(electronics, fR):
    pSupplyOff(electronics[3])
    fR.write(("{0:d},{2:.4f}").format(int(time_now), float(i)))
    pSupplyOn(electronics[3])
    fR.write(("{0:d},{2:.4f}").format(int(time_now), float(i)))
    
def dResist(electronics, fR):
    eLoadOff(electronics[0])
    fR.write(("{0:d},{2:.4f}").format(int(time_now), float(i)))
    eLoadOn(electronics[0])
    fR.write(("{0:d},{2:.4f}").format(int(time_now), float(i)))

def allOff(eLoad, pSupply):
    eLoadOff(eLoad)
    pSupplyOff(pSupply)
    
def eLoadSetup(eLoad):
    eLoadCCMode(eLoad)
    eLoadSetI(eLoad, 3)
    eLoadOn(eLoad)

def pSupplySetup(pSupply):
    pSupplySetV(pSupply, 4.2)
    pSupplySetI(pSupply, 1)
    pSupplyOn(pSupply)

def getVIData(mMeter1, mMeter2):
    v = mMeterGetV(mMeter1)
    i = mMeterGetI(mMeter2)
    print("Volts: {0} Current: {1}\n".format(v,i))
    return v,i

def checkIssues(mMeter1, mMeter2):
    print("temp")