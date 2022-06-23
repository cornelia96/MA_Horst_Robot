# coding = utf-8
# Required modules are inserted and configured
import time
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BCM)
from datetime import datetime, timedelta
import pandas as pd
 
# The respective input / output pins can be selected here
Trigger_AusgangsPin = 15
Echo_EingangsPin = 18
 
# The pause between the individual measurements can be set here in seconds
sleeptime = 1
 
# The input / output pins are configured here
GPIO.setup (Trigger_AusgangsPin, GPIO.OUT)
GPIO.setup (Echo_EingangsPin, GPIO.IN)
GPIO.output (Trigger_AusgangsPin, False)

timestamps = []
datalist = []

full_run = time.time() + 60
 
# Main program loop
try:
    while time.time() < full_run:
        starttime = datetime.now()
        print(starttime)
        # Distance measurement is started by means of the 10us long trigger signal
        GPIO.output (Trigger_AusgangsPin, True)
        time.sleep (0.00001)
        GPIO.output (Trigger_AusgangsPin, False)
 
        # The stopwatch is started here
        switch_on_time = time.time ()
        while GPIO.input (Echo_EingangsPin) == 0:
            switch_on_time = time.time () # The current time is saved until the signal is activated
 
        while GPIO.input (Echo_EingangsPin) == 1:
            switch_off_time = time.time () # The last time when the signal was active is recorded
 
        # The difference between the two times gives the duration you are looking for
        duration = switch_off_time - switch_on_time
        # This can now be used to calculate the distance based on the speed of sound
        distance = (duration * 34300) / 2
 
        # Check whether the measured value is within the permissible distance
        if distance <2 or (round (distance)> 300):
            # If not, an error message is issued
            print ("distance outside the measuring range")
            print ("------------------------------")
        else:
            # The space is formatted to two places behind the comma
            distance = format ((duration * 34300) / 2, '.2f')
            # The calculated distance is output on the console
            datalist.append(distance)
            timestamps.append(starttime.strftime("%H:%M:%S"))
 
        # Pause between the individual measurements
        endtime = datetime.now()
        time_used = endtime - starttime
        time.sleep(sleeptime-time_used.total_seconds())
 
# Clean up after the program has ended
except KeyboardInterrupt:
    GPIO.cleanup ()

df=pd.DataFrame(datalist, index=timestamps, columns=['Distance [m]'])

df.to_excel("/home/cornelia/Documents/Sensortests_1/Data/050/050_ultrasonic_5.xlsx")