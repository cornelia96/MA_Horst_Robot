# Benoetigte Module werden importiert und eingerichtet
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
  
# Hier wird der Eingangs-Pin deklariert, an dem der Sensor angeschlossen ist. Zusaetzlich wird auch der PullUP Widerstand am Eingang aktiviert
LED_PIN = 15
GPIO.setup(LED_PIN, GPIO.OUT, initial= GPIO.LOW)

INPUT_PIN = 14
GPIO.setup(INPUT_PIN, GPIO.IN) 
  
print("LED-Test [druecken Sie STRG+C, um den Test zu beenden]")
 
# Hauptprogrammschleife
try:
        while True:
                print("LED 4 Sekunden an")
                GPIO.output(LED_PIN,GPIO.HIGH) #LED wird eingeschaltet
                if GPIO.input(INPUT_PIN):
                        print("LED IST AN")
                else:
                        print("LED NICHT AN")
                time.sleep(4) #Wartemodus fuer 4 Sekunden
                print("LED 2 Sekunden aus") 
                if GPIO.input(INPUT_PIN):
                        print("LED IST NOCH AN")
                else:
                        print("LED NICHT MEHR AN")
                GPIO.output(LED_PIN,GPIO.LOW) #LED wird ausgeschaltet
                time.sleep(2) #Wartemodus fuer weitere zwei Sekunden, in denen die LED Dann ausgeschaltet ist
  
# Aufraeumarbeiten nachdem das Programm beendet wurde
except KeyboardInterrupt:
        GPIO.cleanup()