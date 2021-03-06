# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:52:49 2019

@author: bwhitehe
"""
import sys
from pathlib import Path

#C:\\Users\\bwhitehe\\Desktop\\BatteryCharacterizerPyVISA-master\\
def makeChargeFiles(argv,state,cycle):
    filepath =  str(Path(__file__).parent.absolute())+ "\\{0}_Data\\{1}{2}.csv".format(sys.argv[1],state,cycle+1)
    fVI = open(filepath, "w")
    fVI.write("Time(s),Volt(v),Current(A)\n")
    filepath =  str(Path(__file__).parent.absolute()) +"\\{0}_Data\\{1}R{2}.csv".format(sys.argv[1],state,cycle+1)
    fR = open(filepath, "w")
    fR.write("Time,Volt,Current,Volt,Current,Volt,Current\n")
    return fVI, fR

def closeFile(fVI,fR):
    fVI.close()
    fR.close()
    
def openCloseFile(fVI,fR,argv,state,cycle):
    fVI.close()
    filepath =  str(Path(__file__).parent.absolute())+"\\{0}_Data\\{1}{2}.csv".format(sys.argv[1],state,cycle+1)
    fVI = open(filepath, "a")
    fR.close()
    filepath =  str(Path(__file__).parent.absolute())+"\\{0}_Data\\{1}R{2}.csv".format(sys.argv[1],state,cycle+1)
    fR = open(filepath, "a")
    return fVI, fR