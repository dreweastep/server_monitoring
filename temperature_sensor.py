# temperature_sensor.py
#
# Created by Drew Eastep
#
# Update log:
#
# 10/23/17 -- Created file
#
# 11/06/2017 -- Copied device serial number
#
# 11/13/2017 -- Adding code for second sensor and edited data
#
# 11/27/2017 -- Added serial code for second sensor
#
# 01/22/2018 -- Added SMTP email alerts
#
# 02/08/2018 -- Changed SMTP to send from internal dunwoody mail sensor with fake address.
#
# 03/22/2018 -- Code now takes in multiple values and sends emails only if multiple high readings are read.
#
# 03/29/2018 -- Fixed logical and syntax bugs
#
# 04/23/2018 -- Added MIME extension to properly format email
#
# 05/10/2018 -- Added log file

# Recording temperature using ds18b20 sensor

import os
import datetime
import time
import smtplib
from email.mime.text import MIMEText

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor_1 = '/sys/bus/w1/devices/28-031722a436ff/w1_slave'
temp_sensor_2 = '/sys/bus/w1/devices/28-03172293f1ff/w1_slave'

file_path = "temp_log.txt"

SERVER = "braincoral.dunwoody.tec.mn.us"
FROM = 'opensourcepialerts@example.com'
SUBJECT = "Temperature Alert!!"
TO = ['cgabrielson@dunwoody.edu', 'easandb@dunwoody.edu', 'rbentz@dunwoody.edu', 'jmcfadden@dunwoody.edu', 'mwederath@dunwoody.edu']


def temp_raw(temp_sensor):
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def send_mail(msg):
    new_message = MIMEText(msg)
    new_message['Subject'] = SUBJECT

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, new_message.as_string())
    server.quit()


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


def count(temp_list, low, high):
    temp_count = 0

    for num in temp_list:
        if low <= num <= high:
            temp_count += 1

    return temp_count


def append_log(file, sensor1_list, sensor2_list):
    with open(file, "a") as data_log:
        data_log.write("\n\n" + str(datetime.datetime.now().strftime("(%Y/%m/%d at %H:%M)")))
        data_log.write("\nSensor 1 temps: " + str(sensor1_list))
        data_log.write("\nSensor 2 temps: " + str(sensor2_list))


sensor1_values = []
sensor2_values = []
to_send_mail = False
message = ""
for i in range(0, 10):
    sensor1_values.append(read_temp(temp_sensor_1)[1])
    sensor2_values.append(read_temp(temp_sensor_2)[1])

append_log(file_path, sensor1_values, sensor2_values)

if count(sensor1_values, 90, 257) > 3:  # Temps above 90 and below 257 fahrenheit -- max value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(max(sensor1_values)) + " degrees fahrenheit from the sensor1 sensor.\n\n"
    to_send_mail = True

if count(sensor2_values, 90, 257) > 3:  # Temps above 90 and below 257 fahrenheit -- max value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(max(sensor2_values)) + " degrees fahrenheit from the sensor2 sensor.\n\n"
    to_send_mail = True

if count(sensor1_values, -67, 36) > 3:  # Temps above -67 and below 40 farenheit -- min value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(min(sensor1_values)) + " degrees fahrenheit from the sensor1 sensor.\n\n"
    to_send_mail = True

if count(sensor2_values, -67, 36) > 3:  # Temps above -67 and below 40 farenheit -- min value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(min(sensor2_values)) + " degrees fahrenheit from the sensor2 sensor.\n\n"
    to_send_mail = True

if to_send_mail:
    send_mail(message)



