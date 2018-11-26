import sys

import Adafruit_DHT

import time

import smtplib

SERVER = "braincoral.dunwoody.tec.mn.us"

FROM = 'opensourcepialerts@example.com'

TO = ['cgabrielson@dunwoody.edu', 'easandb@dunwoody.edu', 'remjamd@dunwoody.edu']                                                                                                       



# Parse command line parameters.


sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

total = 0
for i in range(10):
    
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        total = total + humidity
        time.sleep(10)
            
            
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)

average = total/10
if average > 80 or average < 10:
    #SEND EMAIL
    MESSAGE = "The raspberry pi humidity monitor is reading an average humidity of" + average + "%"

    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, MESSAGE)
    server.quit()
