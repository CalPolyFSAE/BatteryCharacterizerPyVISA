#This file has the settings for the test

#Master Instuctions For Setup:
#Programming Guide: https://docs.google.com/document/d/1mquDV4jmw5xbIG4zOIdvJexC6FVBi6j8p_w1Zlm43iY/edit?usp=sharing

#Ports
ELOADADDRESS = 'GPIB0::1::INSTR'
MMETER1ADDRESS = 'USB0::0x1AB1::0x09C4::DM3R193601853::INSTR' #voltage
MMETER2ADDRESS = 'USB0::0x1AB1::0x09C4::DM3R191700643::INSTR' #current
MMETER3ADDRESS = 'USB0::0x1AB1::0x09C4::DM3R193601754::INSTR' #temp
PSUPPLYADDRESS = 'USB0::0x1AB1::0x0E11::DP8C192803275::INSTR' 

#Electronics Settings in amp and volts
PSUPPLYVOLT = 4.2 
PSUPPLYCURR =  1
ELOADCURR = 3

#Test Settings
CYCLENUM = 1
UPPERVOLTLIMIT = 4.1
LOWERVOLTLIMIT = 2.8
FINALVOLT = 3.8
MAXTEMP = 50


