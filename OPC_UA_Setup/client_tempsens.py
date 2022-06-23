#!usr/bin/env python3

from opcua import Client
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime, timedelta

sleeptime = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print ("Warte auf Initialisierung...")
 
base_dir = '/sys/bus/w1/devices/'
while True:
    try:
        device_folder = glob.glob(base_dir + '28*')[0]
        break
    except IndexError:
        sleep(1)
        continue
device_file = device_folder + '/w1_slave'
 
print('check1')

def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

TemperaturMessung()

def TemperaturAuswertung():
    lines = TemperaturMessung()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

client = Client("opc.tcp://192.168.113.38:3300")
client.connect()

client.get_namespace_array()

objects = client.get_objects_node()

tempsens = objects.get_children()[1]

temperature = tempsens.get_children()[0]

current_temperature = temperature.get_value()

try:
    while True:
        measured_temp = TemperaturAuswertung()
        if current_temperature +0.5 < measured_temp or measured_temp < current_temperature -0.5: 
            temperature.set_value(measured_temp)
except KeyboardInterrupt:
    GPIO.cleanup()