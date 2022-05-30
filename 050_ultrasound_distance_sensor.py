# coding = utf-8
# Required modules are inserted and configured
import time
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BCM)
 
# The respective input / output pins can be selected here
Trigger_AusgangsPin = 27
Echo_EingangsPin = 17
 
# The pause between the individual measurements can be set here in seconds
sleeptime = 0.8
 
# The input / output pins are configured here
GPIO.setup (Trigger_AusgangsPin, GPIO.OUT)
GPIO.setup (Echo_EingangsPin, GPIO.IN)
GPIO.output (Trigger_AusgangsPin, False)
 
# Main program loop
try:
    while True:
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
            fistance = format ((duration * 34300) / 2, '.2f')
            # The calculated distance is output on the console
            print ("The distance is:"), distance, ("cm")
            print ("------------------------------")
 
        # Pause between the individual measurements
        time.sleep (sleeptime)
 
# Clean up after the program has ended
except KeyboardInterrupt:
    GPIO.cleanup ()