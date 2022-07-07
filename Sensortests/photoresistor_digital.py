# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
  
# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist. Zusaetzlich wird auch der PullUP Widerstand am Eingang aktiviert
LED_PIN = 14
GPIO.setup(LED_PIN, GPIO.IN)
  
print("TEEEEST")

try:
    while(True):
        print(f"{datetime.now()}: {GPIO.input(LED_PIN)}")
        time.sleep(1)

except KeyboardInterrupt:
        GPIO.cleanup()