# Prints Temperatures to console in fahrenheit


import os
import time


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor_1 = '/sys/bus/w1/devices/28-031722a436ff/w1_slave'
temp_sensor_2 = '/sys/bus/w1/devices/28-03172293f1ff/w1_slave'


def temp_raw(temp_sensor):

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(temp_sensor):

    lines = temp_raw(temp_sensor)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw(temp_sensor)

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_c, 1), round(temp_f, 1)


for i in range(0, 20):
    print('Sensor 1:', read_temp(temp_sensor_1))
    print('Sensor 2:', read_temp(temp_sensor_2))
    print('')
    time.sleep(5)

print("Done.")