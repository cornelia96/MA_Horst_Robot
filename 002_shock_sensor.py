# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import pandas as pd
   
GPIO.setmode(GPIO.BCM)
   
# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist. Zusaetzlich wird auch der PullUP Widerstand am Eingang aktiviert
GPIO_PIN = 15 
GPIO.setup(GPIO_PIN, GPIO.IN)

timestamps = []
datalist = []
   
print("Sensor-Test [druecken Sie STRG+C, um den Test zu beenden]")
   
# Diese AusgabeFunktion wird bei Signaldetektion ausgefuehrt
def ausgabeFunktion(null):
        timestamps.append(datetime.now())
        datalist.append(1)
        print("Signal erkannt")
   
# Beim Detektieren eines Signals (fallende Signalflanke) wird die Ausgabefunktion ausgeloest
GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING, callback=ausgabeFunktion, bouncetime=100) 
   
# Hauptprogrammschleife

try:
    while True:
        timestamps.append(datetime.now())
        datalist.append(0)
        time.sleep(1)
   
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()

        df=pd.DataFrame(datalist, index=timestamps, columns=['Signal'])

        df.to_excel("/home/cornelia/Documents/Sensortests_1/Data/002/002_shock_1.xlsx")
