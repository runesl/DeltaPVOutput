#A simple script to read values from a delta inverter and post them to 
#PVoutput.org

import time, subprocess,serial
from deltaInv import DeltaInverter
from time import localtime, strftime

#PVOutput.org API Values - UPDATE THESE TO YOURS!
SYSTEMID=""
APIKEY=""

if __name__ == '__main__':

    #Edit your serial connection as required!!
    connection = serial.Serial('/dev/ttyUSB0',19200,timeout=0.2);
    localtime = time.localtime(time.time())   
 
    t_date = 'd={0}'.format(strftime('%Y%m%d'))
    t_time = 't={0}'.format(strftime('%H:%M'))

    inv1 = DeltaInverter(1) #init Inverter 1
    #Get the Daily Energy thus far
    cmd = inv1.getCmdStringFor('Day Wh')
    connection.write(cmd)
    response = connection.read(100)
    #if no response the inverter is asleep
    if response:
        value = inv1.getValueFromResponse(response)
        t_energy = 'v1={0}'.format(value)

	#instanteous power
        cmd = inv1.getCmdStringFor('AC Power')
        connection.write(cmd)
        response = connection.read(100)
        value = inv1.getValueFromResponse(response)
        t_power = 'v2={0}'.format(value)

	#AC Voltage
        cmd = inv1.getCmdStringFor('AC Volts')
        connection.write(cmd)
        response = connection.read(100)
        value = inv1.getValueFromResponse(response)
        t_volts = 'v6={0}'.format(value)

	#Temp - this appears to be onboard somewhere not the heatsink
        cmd = inv1.getCmdStringFor('DC Temp')
        connection.write(cmd)
        response = connection.read(100)
        value = inv1.getValueFromResponse(response)
        t_temp = 'v5={0}'.format(value)

	#Send it all off to PVOutput.org
        cmd = ['/usr/bin/curl',
            '-d', t_date,
            '-d', t_time,
            '-d', t_energy,
            '-d', t_power, 
            '-d', t_volts,
            '-d', t_temp,
            '-H', 'X-Pvoutput-Apikey: ' + APIKEY, 
            '-H', 'X-Pvoutput-SystemId: ' + SYSTEMID, 
            'http://pvoutput.org/service/r1/addstatus.jsp']
        ret = subprocess.call (cmd)
    else:
        print "No response from inverter - shutdown? No Data sent to PVOutput.org"
        connection.close()
