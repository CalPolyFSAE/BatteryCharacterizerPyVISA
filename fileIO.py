# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:52:49 2019

@author: bwhitehe
"""
import sys

def makeChargeFiles(argv,state,cycle):
    filepath =  "C:\\Users\\bwhitehe\\Desktop\\BatteryCharacterizerPyVISA-master\\{0}_Data\\{1}{2}.csv".format(sys.argv[1],state,cycle+1)
    fVI = open(filepath, "w")
    fVI.write("Time,Volt,Current\n")
    filepath =  "C:\\Users\\bwhitehe\\Desktop\\BatteryCharacterizerPyVISA-master\\{0}_Data\\{1}R{2}.csv".format(sys.argv[1],state,cycle+1)
    fR = open(filepath, "w")
    fR.write("Time,Volt,Current,Volt,Current,Volt,Current\n")
    return fVI, fR

def closeFile(fVI,fR):
    fVI.close()
    fR.close()