# coding=utf-8
# Benoetigte Module werden importiert und eingerichtet
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import pandas as pd
 
# An dieser Stelle kann die Pause zwischen den einzelnen Messungen eingestellt werden
sleeptime = 1
 
# Der One-Wire EingangsPin wird deklariert und der integrierte PullUp-Widerstand aktiviert
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
# bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist
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
# Funktion wird definiert, mit dem der aktuelle Messwert am Sensor ausgelesen werden kann
def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
# Zur Initialisierung, wird der Sensor einmal "blind" ausgelesen
TemperaturMessung()
 
# Die Temperaturauswertung: Beim Raspberry Pi werden erkennte one-Wire Slaves im Ordner
# /sys/bus/w1/devices/ einem eigenen Unterordner zugeordnet. In diesem Ordner befindet sich die Datei w1-slave
# in dem Die Daten, die über dem One-Wire Bus gesendet wurden gespeichert.
# In dieser Funktion werden diese Daten analysiert und die Temperatur herausgelesen und ausgegeben
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
 
# Hauptprogrammschleife
# Die gemessene Temperatur wird in die Konsole ausgegeben - zwischen den einzelnen Messungen
# ist eine Pause, deren Länge mit der Variable "sleeptime" eingestellt werden kann

timestamps = []
datalist = []

full_run = time.time() + 60*3

try:
    print('check')
    while time.time() < full_run:
        starttime = datetime.now()
        print(starttime)
        datalist.append(TemperaturAuswertung())
        timestamps.append(starttime.strftime("%H:%M:%S"))
        endtime = datetime.now()
        time_used = endtime - starttime
        time.sleep(sleeptime-time_used.total_seconds())
 
except KeyboardInterrupt:
    GPIO.cleanup()



df=pd.DataFrame(datalist, index=timestamps, columns=['Temperature [C]'])

df.to_excel("/home/cornelia/Documents/Sensortests_1/Data/001/001_temp_5.xlsx")