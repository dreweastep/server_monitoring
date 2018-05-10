# Test for temperature_sensor.py


import datetime
import smtplib
from email.mime.text import MIMEText

file_path = "temp_log.txt"

SERVER = "braincoral.dunwoody.tec.mn.us"
FROM = 'opensourcepialerts@example.com'
SUBJECT = "THIS IS A TEST"
TO = ['cgabrielson@dunwoody.edu', 'easandb@dunwoody.edu', 'smekylg@dunwoody.edu', 'remjamd@dunwoodyedu']


def temp_raw(temp_sensor):

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines


def send_mail(message):

    MESSAGE = MIMEText(message)
    MESSAGE['Subject'] = SUBJECT

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, MESSAGE.as_string())
    server.quit()


def count(temp_list, low, high):
    temp_count = 0

    for num in temp_list:
        if low <= num <= high:
            temp_count+= 1

    return temp_count


def append_log(file, sensor1_list, sensor2_list):
    with open(file, "a") as data_log:
        data_log.write("\n\n" + str(datetime.datetime.now().strftime("(%Y/%m/%d at %H:%M)")))
        data_log.write("\nSensor 1 temps: " + str(sensor1_list))
        data_log.write("\nSensor 2 temps: " + str(sensor2_list))


sensor1_values = [98, 93, 45, 94, 90, 54, 32, 76, 88]
sensor2_values = [98, 93, 45, 94, 90, 54, 32, 76, 88, 100]
to_send_mail = False
message = ""

append_log(file_path, sensor1_values, sensor2_values)

if count(sensor1_values, 90, 257) > 3:  # Temps above 90 and below 257 fahrenheit -- max value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(max(sensor1_values)) + " degrees fahrenheit from the sensor1 sensor.\n\n"
    to_send_mail = True

if count(sensor2_values, 90, 257) > 3:  # Temps above 90 and below 257 fahrenheit -- max value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(max(sensor2_values)) + " degrees fahrenheit from the sensor2 sensor.\n\n"
    to_send_mail = True

if count(sensor1_values, -67, 42) > 3:  # Temps above -67 and below 42 farenheit -- min value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(min(sensor1_values)) + " degrees fahrenheit from the sensor1 sensor.\n\n"
    to_send_mail = True

if count(sensor2_values, -67, 42) > 3:  # Temps above -67 and below 42 farenheit -- min value from sensor
    message = message + "The raspberry pi temperature monitor is reading a temperature of " \
              + str(min(sensor2_values)) + " degrees fahrenheit from the sensor2 sensor.\n\n"
    to_send_mail = True

if to_send_mail:
    send_mail(message)
