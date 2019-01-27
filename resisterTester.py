import visa
import time

rm = visa.ResourceManager()
print(rm.list_resources())

pSupply = rm.open_resource('COM3')
pSupply.baud_rate = 57600

print("-----------------------")

pSupply.write("CURR 40")
pSupply.write("OUT 1")
start_time = time.time()
v = pSupply.query("VOUT?")

while(float(v) <= 18):
     v = pSupply.query("VOUT?")
print("Final Time in Seconds: {0}".format(time.time()-start_time))
pSupply.write("OUT 0")
pSupply.close()







#count = 0
#if(count%50 == 0):
         #print("Volts: {0} Time: {1}\n".format(v,time.time()-start_time))
     #count += 1