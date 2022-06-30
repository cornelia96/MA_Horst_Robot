#!usr/bin/env python3

from opcua import Client
import glob
import RPi.GPIO as GPIO
from time import sleep
import constants


client = Client(f"opc.tcp://{constants.ip_address}:3300")
client.connect()

client.get_namespace_array()

objects = client.get_objects_node()

shocksensor = objects.get_children()[2]

shock_detected = shocksensor.get_children()[0]

GPIO.setmode(GPIO.BCM)
   
# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist. Zusaetzlich wird auch der PullUP Widerstand am Eingang aktiviert
GPIO_PIN = constants.shocksens_pin
GPIO.setup(GPIO_PIN, GPIO.IN)
   
# Diese AusgabeFunktion wird bei Signaldetektion ausgefuehrt
def ausgabeFunktion(null):
        shock_detected.set_value(True)
        sleep(1)
        shock_detected.set_value(False)
   
# Beim Detektieren eines Signals (fallende Signalflanke) wird die Ausgabefunktion ausgeloest
GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=ausgabeFunktion, bouncetime=100) 
   
# Hauptprogrammschleife

try:
    while True:
        sleep(1)
   
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()

