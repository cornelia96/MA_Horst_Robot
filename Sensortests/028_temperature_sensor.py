#!/usr/bin/python
# coding=utf-8
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Create the I2C bus

delayTime = 1
Digital_PIN = 24

GPIO.setup(Digital_PIN, GPIO.IN, pull_up_down = GPIO.PUD_OFF)
i=1
while True:
    print(i)
    i+=1
    time.sleep(delayTime)
    # Ausgabe auf die Konsole
    if GPIO.input(Digital_PIN) == False:
        print ("Grenzwert: noch nicht erreicht")
    else:
        print ("Grenzwert: erreicht")
        print ("------------- --------------------------")

    

